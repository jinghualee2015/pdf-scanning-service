import time
import os

from pdf_ocr_service.jobs.processors.base_processor import BaseDocumentProcessor
from pdf_ocr_service.jobs.domains import DocumentPdfExtractTaskInfo
from pdf_ocr_service.celery import task_logger

logger = task_logger


class PdfExtractTaskProcessor(BaseDocumentProcessor):
    """
    extract Pdf document content
    """

    def __init__(self,
                 task_info: DocumentPdfExtractTaskInfo = None):
        super(PdfExtractTaskProcessor, self).__init__(task_info=task_info)

    def business_process(self):
        try:
            self.process_result.set_status(True)
            self.process_result.set_error_msg('')
            self.pull_source_pdf()
            self.read_content()
        except Exception as e:
            message = ",".join(str(i) for i in e.args)
            self.process_result.set_status(False)
            self.process_result.set_error_msg(message)
        finally:
            self.generate_summary()
            self.generate_tokens()
            self.notify_result()
            self.clear_tmp_file()

    def read_content(self):
        self._extract()

    def _extract(self):
        logger.info(f"begin extract document:[{self.task_info.document_id}] pdf file ...")
        start_time = time.time()
        tmp_input = os.path.join(self.task_info.tmp_dir, self.task_info.tmp_source_file_name)
        try:
            self.extract_pages(tmp_input)
        except Exception as ex:
            import traceback
            error = traceback.format_exc()
            logger.error(f"extract pdf:{tmp_input}\n occur error:{error}")
            raise Exception(error)
        finally:
            self.process_result.set_file_path(self.task_info.source_file)
            self.process_result.set_side_car_path('')
            end_time = time.time()
            logger.info(
                f"finish extract document:[{self.task_info.document_id}] use time:[{end_time - start_time}] seconds")
