import os
import unittest

from pdf_ocr_service.jobs.extractors import BasePdfExtractor, CompositePdfExtractor


class CompositePdfExtractorTest(unittest.TestCase):
    def setUp(self):
        self.extractor: BasePdfExtractor = CompositePdfExtractor()

    def test_extract(self):
        pdf_path = os.path.join(os.path.dirname(__file__), "../examples", "71017.pdf")
        self.extractor.init_pdf(pdf_file=pdf_path)
        result: dict = self.extractor.extract_page()
        print(result.get('content'))
        # for token in result.get('pages'):
        #     print(token)

        positions = self.extractor.extract_position(6, "FDA recognizes that the experimental nature of the drug")
        print(positions)

    def test_extract2(self):
        pdf_path = os.path.join(os.path.dirname(__file__), "../examples", "pdf-3.pdf")
        self.extractor.init_pdf(pdf_file=pdf_path)
        result: dict = self.extractor.extract_page()
        # print(result.get('content'))
        # for token in result.get('pages'):
        #     print(token)
        # BK (10 /H9262M), Lys-des[Arg9]-BK (10 /H9262M), or PAF (1 /H9262M; positive control).
        positions = self.extractor.extract_position(1, "BK (10 �M), Lys-des[Arg9]-BK (10 �M), or PAF (1 �M; positive control).")
        print(positions)
