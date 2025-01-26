import os

from pdf_ocr_service.factory.app_factory import service_config
from pdf_ocr_service.jobs.domains import DocumentOfficeTaskInfo
from pdf_ocr_service.jobs.processors import PdOcrfTaskProcessor, PdfExtractTaskProcessor, OfficeExtractTaskProcessor
from pdf_ocr_service.jobs.domains.document_pdf_task_info import DocumentPdfOcrTaskInfo, DocumentPdfExtractTaskInfo
import unittest


class TestProcessor(unittest.TestCase):
    def setUp(self):
        pass

    def test_pdf_ocr(self) -> None:
        """
        测试OCR任务是否正常工作
        """
        task_dict = dict(
            document_id=128,
            version=1,
            task_id='23-e23e9f69cd774e81b319e9014961b6ca',
            source_file='dev/pdf/ocr/128/V00001/128-1-original.pdf',
            target_path='dev/pdf/ocr/128/V00002',
            target_file_name='20231212-0011',
            language='eng',
            bucket_name='dms-us-east2',
            retry=0,
            max_retries=3,
            task_key='pdf_ocr',
            task_name='pdf_ocr_service.jobs.tasks.ocr_pdf_document',
            queue_name='pdf-ocr',

        )
        from pdf_ocr_service.jobs.tasks import ocr_pdf_document
        result = ocr_pdf_document.apply(args=(task_dict,))
        result.get()

        # document_id = task_dict.get('document_id')
        # version = task_dict.get('version')
        # task_id = task_dict.get('task_id')
        # tmp_dir = os.path.join(service_config.tmp_pdf_path, task_id)
        #
        # task_info = DocumentPdfOcrTaskInfo(
        #     task_params=task_dict,
        #     document_id=document_id,
        #     task_id=task_dict.get('task_id'),
        #     version=version,
        #     source_file=task_dict.get('source_file'),
        #     language=task_dict.get('language'),
        #     target_path=task_dict.get('target_path'),
        #     target_file_name=task_dict.get('target_file_name'),
        #     tmp_dir=tmp_dir,
        #     bucket_name=task_dict.get('bucket_name'),
        # )
        #
        # processor = PdOcrfTaskProcessor(task_info=task_info)
        # processor.process()

    def test_pdf_extract(self) -> None:
        """
        测试OCR任务是否正常工作
        """
        task_dict = dict(
            document_id=2292,
            version=2,
            task_id='17-9a85d41fd88743e788eb3ba2ddedd99c',
            source_file='dev/office/extract/2291/V00001/parsed/2291_1.pdf',
            target_path='dev/pdf/extract/2292/V00002/',
            target_file_name='2291_1.pdf',
            language='eng',
            bucket_name='dms-us-east2',
            retry=0,
            max_retries=0,
            task_key='pdf_extractor',
            task_name='pdf_ocr_service.jobs.tasks.extract_pdf_document',
            queue_name='pdf_extractor',

        )

        document_id = task_dict.get('document_id')
        version = task_dict.get('version')
        task_id = task_dict.get('task_id')
        tmp_dir = os.path.join(service_config.tmp_pdf_path, task_id)

        task_info = DocumentPdfExtractTaskInfo(
            task_params=task_dict,
            document_id=document_id,
            task_id=task_dict.get('task_id'),
            version=version,
            source_file=task_dict.get('source_file'),
            language=task_dict.get('language'),
            target_path=task_dict.get('target_path'),
            tmp_dir=tmp_dir,
            bucket_name=task_dict.get('bucket_name'),
        )

        processor = PdfExtractTaskProcessor(task_info=task_info)
        processor.process()

    def test_pdf_ocr(self) -> None:
        """
        测试OCR任务是否正常工作
        """
        task_dict = dict(
            document_id=2195,
            version=1,
            task_id='9-43b840f7c9af4fce863994b14468ff7d',
            source_file='dev/pdf/extract/2270/V00001/original/71017.pdf',
            target_path='dev/pdf/ocr/128/V00002',
            target_file_name='20231212-0011',
            language='eng',
            bucket_name='dms-us-east2',
            retry=0,
            max_retries=3,
            task_key='pdf_extractor',
            task_name='pdf_ocr_service.jobs.tasks.extract_office_document',
            queue_name='pdf_extractor',

        )

        document_id = task_dict.get('document_id')
        version = task_dict.get('version')
        task_id = task_dict.get('task_id')
        tmp_dir = os.path.join(service_config.tmp_pdf_path, task_id)

        task_info = DocumentPdfOcrTaskInfo(
            task_params=task_dict,
            document_id=document_id,
            task_id=task_dict.get('task_id'),
            version=version,
            source_file=task_dict.get('source_file'),
            language=task_dict.get('language'),
            target_path=task_dict.get('target_path'),
            tmp_dir=tmp_dir,
            bucket_name=task_dict.get('bucket_name'),
            target_file_name='20231212-0011',
        )

        processor = PdOcrfTaskProcessor(task_info=task_info)
        processor.process()

    def test_office_extract(self) -> None:
        """
        测试OCR任务是否正常工作
        """
        task_dict = dict(
            document_id=2195,
            version=1,
            task_id='50-ae93dc813f394ce48435c92e93841cde',
            source_file='dev/pdf/ocr/2270/V00001/71017.pdf',
            target_path='dev/pdf/ocr/128/V00002',
            target_file_name='20231212-0011',
            language='eng',
            bucket_name='dms-us-east2',
            retry=0,
            max_retries=3,
            task_key='pdf_extractor',
            task_name='pdf_ocr_service.jobs.tasks.extract_office_document',
            queue_name='pdf_extractor',

        )

        document_id = task_dict.get('document_id')
        version = task_dict.get('version')
        task_id = task_dict.get('task_id')
        tmp_dir = os.path.join(service_config.tmp_pdf_path, task_id)

        task_info = DocumentOfficeTaskInfo(
            task_params=task_dict,
            document_id=document_id,
            task_id=task_dict.get('task_id'),
            version=version,
            source_file=task_dict.get('source_file'),
            language=task_dict.get('language'),
            target_path=task_dict.get('target_path'),
            tmp_dir=tmp_dir,
            bucket_name=task_dict.get('bucket_name'),
        )

        processor = OfficeExtractTaskProcessor(task_info=task_info)
        processor.process()

    def test_task(self) -> None:
        """
        测试OCR任务是否正常工作
        """
        task_dict = dict(
            document_id=128,
            version=1,
            task_id='dafdsfsdsdafasdfdsafsdaf',
            source_file='dev/pdf/ocr/128/V00001/128-1-original.pdf',
            target_path='dev/pdf/ocr/128/V00002',
            target_file_name='20231212-0011',
            language='eng',
            bucket_name='dms-us-east2',
            retry=0,
            max_retries=3,
            task_key='ocfpdf',
            task_name='pdf_ocr_service.jobs.ocr.jobs.ocr_pdf',
            queue_name='pdf-ocr',

        )

        document_id = task_dict.get('document_id')
        version = task_dict.get('version')
        task_id = task_dict.get('task_id')
        tmp_dir = os.path.join(service_config.tmp_pdf_path, task_id)

        task_info = DocumentPdfOcrTaskInfo(
            task_params=task_dict,
            document_id=document_id,
            task_id=task_dict.get('task_id'),
            version=version,
            source_file=task_dict.get('source_file'),
            language=task_dict.get('language'),
            target_path=task_dict.get('target_path'),
            target_file_name=task_dict.get('target_file_name'),
            tmp_dir=tmp_dir,
            bucket_name=task_dict.get('bucket_name'),
        )

        print(task_info.get_target_pdf_file)
        print(task_info.get_target_text_file)

    def test_not_pdf(self):
        """
        :return:
        """
        task_dict = dict(
            document_id=81,
            version=1,
            task_id='dafdsfsdsdafasdfdsafsdaf',
            source_file='/ocr/pdf/unit-test/archery-api.pdf',
            target_path='/dev/pdf/81/v00002/',
            target_file_name='20231110-111',
            language='eng',
            bucket_name='dms-us-east2',
            retry=0,
            max_retries=3,
            task_key='ocfpdf',
            task_name='pdf_ocr_service.jobs.ocr.jobs.ocr_pdf',
            queue_name='pdf-ocr',

        )

        document_id = task_dict.get('document_id')
        version = task_dict.get('version')
        task_id = task_dict.get('task_id')
        tmp_dir = os.path.join(service_config.tmp_pdf_path, task_id)

        task_info = DocumentPdfOcrTaskInfo(
            task_params=task_dict,
            document_id=document_id,
            task_id=task_dict.get('task_id'),
            version=version,
            source_file=task_dict.get('source_file'),
            language=task_dict.get('language'),
            target_path=task_dict.get('target_path'),
            target_file_name=task_dict.get('target_file_name'),
            tmp_dir=tmp_dir,
            bucket_name=task_dict.get('bucket_name'),
        )

        processor = PdOcrfTaskProcessor(task_info=task_info)
        processor.process()
