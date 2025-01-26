from abc import ABCMeta, abstractmethod
from pdf_ocr_service.jobs.domains import TokenPosition


class BasePdfExtractor(metaclass=ABCMeta):
    def __init__(self):
        self.pdf_file = None
        self.pdf_obj = None

    @abstractmethod
    def init_pdf(self, pdf_file: str = None):
        pass

    @abstractmethod
    def extract_page(self) -> dict:
        pass

    @abstractmethod
    def extract_position(self,
                         page_number: int = None,
                         token: str = None,
                         ) -> list[TokenPosition]:
        pass


