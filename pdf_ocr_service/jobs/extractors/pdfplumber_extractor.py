import pdfplumber

from pdf_ocr_service.celery import task_logger
from pdf_ocr_service.jobs.domains import TokenPosition
from pdf_ocr_service.jobs.extractors import BasePdfExtractor

logger = task_logger


class PdfPlumberExtractor(BasePdfExtractor):
    def init_pdf(self, pdf_file: str = None):
        self.pdf_file = pdf_file
        self.pdf_obj = pdfplumber.open(self.pdf_file)

    def extract_page(self) -> dict:
        result = {}
        content = ''
        pages = []
        for page in self.pdf_obj.pages:
            page_content = page.extract_text()
            content = content + page_content
            page_info = {
                "content": page_content,
                "page": page.page_number - 1
            }
            pages.append(page_info)
        result['content'] = content
        result['pages'] = pages
        return result

    def extract_position(self,
                         page_number: int = None,
                         token: str = None, ) -> list[TokenPosition]:
        result: list[TokenPosition] = []
        page = self.pdf_obj.pages[page_number]
        search_result = page.search(token,
                                    regex=False,
                                    case=True,
                                    return_chars=False,
                                    return_groups=False)
        if search_result is None or len(search_result) <= 0:
            logger.warn(f"extract_position due to search_result is none or no data just return empty list")
            return result
        for result in search_result:
            left: float = result.get('x0')
            right: float = result.get('x1')
            top: float = result.get('top')
            bottom: float = result.get('bottom')
            logger.debug(f"page:{page} token:{token} with position:{left},{right},{top},{bottom}")
            position: TokenPosition = TokenPosition(left, right, top, bottom)
            if position.is_valid():
                result.append(position)
            else:
                logger.warn(
                    f"_generate_position due to result has null element {result} just skip this position.")
        return result

    def __del__(self):
        self.pdf_file = None
        if self.pdf_obj is not None:
            self.pdf_obj.close()
