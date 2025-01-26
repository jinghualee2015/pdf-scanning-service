import os
import unittest

from celery.utils.log import get_logger

from pdf_ocr_service.jobs.extractors import BasePdfExtractor, PyPdfExtractor

logger = logger = get_logger("py-pdf-extractor")


class PyPdfExtractorTest(unittest.TestCase):
    def setUp(self):
        self.extractor: BasePdfExtractor = PyPdfExtractor()

    def test_extract(self):
        pdf_path = os.path.join(os.path.dirname(__file__), "../examples", "71017.pdf")
        self.extractor.init_pdf(pdf_file=pdf_path)
        result: dict = self.extractor.extract_page()
        # print(result.get('content'))
        for token in result.get('pages'):
            logger.info(token)

    def test_logs(self):
        logger.info("hello word!!!!")
