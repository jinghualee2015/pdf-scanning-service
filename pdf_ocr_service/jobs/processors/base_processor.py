import os
from abc import abstractmethod, ABCMeta
import shutil
import json
import boto3
import time

from langchain.text_splitter import RecursiveCharacterTextSplitter

from pdf_ocr_service.factory.app_factory import service_config

from pdf_ocr_service.jobs.domains import DocumentTaskInfo, DocumentProcessResult, EmbeddingToken, TokenPosition
from pdf_ocr_service.jobs.db import update_process_content
from pdf_ocr_service.celery import task_logger
import numpy as np

from pdf_ocr_service.jobs.extractors import BasePdfExtractor, PyMupdfExtractor

logger = task_logger


class BaseDocumentProcessor(metaclass=ABCMeta):
    """
    Base Document Processor class
    """

    def __init__(self,
                 task_info: DocumentTaskInfo = None
                 ):
        self.task_info = task_info
        self.bucket_name = task_info.bucket_name
        self.process_result = DocumentProcessResult(
            document_id=task_info.document_id,
            version=task_info.version,
            task_id=task_info.task_id,
        )
        self._text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1500,
            chunk_overlap=500,
        )
        self._summary_splitter = RecursiveCharacterTextSplitter(
            chunk_size=45000,
            chunk_overlap=9000,
        )
        session = boto3.Session(
            aws_access_key_id=service_config.ai_config.access_key,
            aws_secret_access_key=service_config.ai_config.secret_key,
            region_name=service_config.ai_config.region_name,
        )
        self._brt = session.client(service_name=service_config.ai_config.service_name)
        self.extractor: BasePdfExtractor = PyMupdfExtractor()

    def process(self):
        task_name = self.__class__.__name__
        task_id = self.task_info.task_id
        logger.info('{0} begin process task {1}....'.format(task_name, task_id))
        start_time = time.time()
        self.business_process()
        over_time = time.time()
        logger.info('{0} proces task {1}  completed with use [{2}] seconds'.format(task_name, task_id,
                                                                                   (over_time - start_time)))

    @abstractmethod
    def business_process(self):
        pass

    @abstractmethod
    def read_content(self):
        """
        read document content and parsed document content into tokens
        :return:
        """
        pass

    def extract_pages(self, input_file: str = None):
        """Extract page information for input_file"""
        content = ''
        if os.path.exists(input_file) and os.path.isfile(input_file):
            try:
                input_file = input_file.__str__()
                self.extractor.init_pdf(input_file)
                extract_result: dict = self.extractor.extract_page()
                content = extract_result.get('content')  # self._extract_page_with_pdf_plumber(input_file=input_file)
                self.process_result.add_all_page_content(extract_result.get('pages'))
            except Exception:
                content = ''
                import traceback
                error = traceback.format_exc()
                logger.error(f"extract pages for document[{self.task_info.document_id}] occur error:{error} ")
        else:
            logger.warn(
                f"extract pages for document[{self.task_info.document_id}] failed due to file [{input_file}] not exits.")
        self.process_result.set_content(content if content is not None else '')

    def pull_source_pdf(self, ) -> str:
        logger.info(f"begin pull source file [{self.task_info.source_file}] from storage...")
        result = service_config.oss_cfg.get_bucket_file(bucket_name=self.bucket_name,
                                                        object_name=self.task_info.source_file,
                                                        store_dir=self.task_info.tmp_dir,
                                                        store_file_name=self.task_info.tmp_source_file_name
                                                        )
        logger.info(f"finish pull source file [{self.task_info.source_file}] from storage...")
        return result

    def notify_result(self):
        logger.info(f"begin notify_result, process result... ")
        result = update_process_content(self.process_result)
        logger.info(f"finish notify_result result is {result} ")

    def generate_summary(self):
        """
        generate document summary information
        :return: None
        """
        logger.info(f"begin generate summary for document [{self.task_info.document_id}]...")
        if self.process_result.get_content() is None or len(self.process_result.get_content()) == 0:
            logger.warning(
                f"due to document[{self.task_info.document_id}] content is empty terminate the generate summary process.")
            return
        start_time = time.time()
        pages_split = self._summary_splitter.split_text(self.process_result.get_content())
        # call ai api to generate summary
        summaries = []
        final_template = "\n\nHuman: Act as an expert in life science. The following is set of summaries. Please write a final, consolidated summary of them.\n<summary>\n{info}\n</summary>\n\nAssistant:"
        page_template = "\n\nHuman: Act as an expert in life science. Please write a concise summary of the following text.\n<text>\n{info}\n</text>\n\nAssistant:"
        if len(pages_split) == 1:
            final_summary = self._generate_summary(page_template, pages_split[0])
        else:
            for sum_text in pages_split:
                summary = self._generate_summary(page_template, sum_text)
                summaries.append(summary)
            text_lst = [t.strip() for t in summaries]
            text = '\n\n'.join(text_lst)
            final_summary = self._generate_summary(final_template, text)
        self.process_result.set_summary(final_summary)
        end_time = time.time()
        logger.info(
            f"finish generate summary  for document:[{self.task_info.document_id}] use time:[{end_time - start_time}] seconds")

    def _generate_summary(self, template, content):
        tokens = content.strip()
        prompt = template.format(info=tokens)
        body = json.dumps({"prompt": prompt,
                           "max_tokens_to_sample": service_config.ai_config.summary_info.max_tokens_to_sample,
                           "temperature": service_config.ai_config.summary_info.temperature,
                           "stop_sequences": service_config.ai_config.summary_info.stop_sequences
                           })

        model_id = service_config.ai_config.summary_info.model_id
        accept = service_config.ai_config.accept
        content_type = service_config.ai_config.content_type
        response = self._brt.invoke_model(body=body, modelId=model_id, accept=accept, contentType=content_type)
        response_body = json.loads(response.get('body').read())
        summary = response_body.get('completion')
        logger.debug(f"generate summary:{summary}")
        return summary

    def generate_tokens(self):
        """
        generate document target version embedding information
        this operation will batch delete old embedding information and insert news
        or just batch insert new embeddings
        :return: None
        """
        logger.info(f"begin generate embeddings for document [{self.task_info.document_id}]...")
        if self.process_result.get_page_contents() is None or len(self.process_result.get_page_contents()) == 0:
            logger.warning(
                f"due to document[{self.task_info.document_id}] content is empty terminate the generate embeddings process.")
            return
        start_time = time.time()
        pages_split = self._text_splitter.split_documents(self.process_result.get_page_contents())

        block_num = 0
        for pages in pages_split:
            block_num = block_num + 1
            page_number = int(pages.metadata['page'])
            text_input = pages.page_content
            page_positions = self._generate_positions(page=page_number,
                                                      token=text_input,
                                                      block_numer=block_num,
                                                      process_result=self.process_result)
            self.process_result.add_token(EmbeddingToken(
                page=page_number,
                token=text_input,
                block_num=block_num,
                embeddings=self._generate_embeddings(text_input),
                positions=page_positions
            ))

        end_time = time.time()
        logger.info(
            f"finish generate embeddings for document:[{self.task_info.document_id}] use time:[{end_time - start_time}] seconds")

    def _generate_positions(self, page: int, token, **kwargs) -> list[TokenPosition]:
        positions: list[TokenPosition] = []
        if page < 0 or len(token) <= 0:
            logger.warn(f"_generate_position due to page less 0 or token is empty just return empty list")
            return positions
        return self.extractor.extract_position(page_number=page, token=token, **kwargs)

    def _generate_embeddings(self, tokens):
        tokens = tokens.replace("\x00", "")
        body = json.dumps({
            "texts": [tokens],
            "input_type": service_config.ai_config.embedding_info.input_type
        })
        model_id = service_config.ai_config.embedding_info.model_id
        accept = service_config.ai_config.accept
        content_type = service_config.ai_config.content_type
        response = self._brt.invoke_model(body=body, modelId=model_id, accept=accept, contentType=content_type)
        response_body = json.loads(response.get('body').read())
        embedding = np.array(response_body.get('embeddings')[0])
        logger.debug(f"generate embeddings:{embedding}")
        return embedding

    def clear_tmp_file(self) -> bool:
        tmp_dir = self.task_info.tmp_dir
        logger.info(f"begin clear task document:[{self.task_info.document_id}] temp directory [{tmp_dir}]...")
        if tmp_dir is not None and os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir)
            return True

        logger.info(f"finish clear task document:[{self.task_info.document_id}] temp directory [{tmp_dir}].")
        return False
