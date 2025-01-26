from pypdf import PdfReader

from pdf_ocr_service.celery import task_logger
from pdf_ocr_service.jobs.domains import TokenPosition
from pdf_ocr_service.jobs.extractors import BasePdfExtractor

logger = task_logger


class PyPdfExtractor(BasePdfExtractor):
    def init_pdf(self, pdf_file: str = None):
        self.pdf_file = pdf_file
        self.pdf_obj = PdfReader(self.pdf_file)

    def extract_page(self) -> dict:
        result = {}
        content = ''
        pages = []
        for index, page in enumerate(self.pdf_obj.pages):
            page_content = page.extract_text()
            content = content + page_content
            page_info = {
                "content": page_content,
                "page": page.page_number
            }
            pages.append(page_info)
        result['content'] = content
        result['pages'] = pages
        return result

    def extract_position(self, page_number: int = None, token: str = None) -> list[TokenPosition]:
        raise NotImplementedError

    def __del__(self):
        self.pdf_file = None
        if self.pdf_obj is not None:
            del self.pdf_obj
