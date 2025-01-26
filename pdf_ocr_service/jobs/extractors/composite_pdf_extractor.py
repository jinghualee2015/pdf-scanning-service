from pdf_ocr_service.jobs.domains import TokenPosition
from pdf_ocr_service.jobs.extractors import BasePdfExtractor, PyPdfExtractor, PyMupdfExtractor


class CompositePdfExtractor(BasePdfExtractor):
    def __init__(self):
        self._content_extractor = PyPdfExtractor()
        self._position_extractor = PyMupdfExtractor()

    def init_pdf(self, pdf_file: str = None):
        self._content_extractor.init_pdf(pdf_file=pdf_file)
        self._position_extractor.init_pdf(pdf_file=pdf_file)

    def extract_page(self) -> dict:
        return self._content_extractor.extract_page()

    def extract_position(self, page_number: int = None, token: str = None) -> list[TokenPosition]:
        return self._position_extractor.extract_position(page_number=page_number, token=token)

    def __del__(self):
        self._content_extractor.__del__()
        self._position_extractor.__del__()
