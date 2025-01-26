import json
import unittest
import pdfplumber
import os
import img2pdf
from pypdf import PdfReader

from pdf_ocr_service.jobs.extractors import BasePdfExtractor,PdfPlumberExtractor


class PdfExtractor(unittest.TestCase):
    def setUp(self):
        self.extractor: BasePdfExtractor = PdfPlumberExtractor()

    def test_extract_2(self):
        path = os.path.join(os.path.dirname(__file__), "../examples", "K940242_ocr.pdf")
        pdfReader = PdfReader(path)
        for index, page in enumerate(pdfReader.pages):
            print(index)
            print(page.extract_text())

    def test_extract(self):
        contents = [
            "The sensitivity of this antibody was shown by consistent staining of 9 of 10 breast and 10",
            "Inter-run reproducibility was determined based on samples of the same tissue on 16"
        ]
        path = os.path.join(os.path.dirname(__file__), "../examples", "K940242_ocr.pdf")
        with pdfplumber.open(path) as pdf:
            pages = pdf.pages
            for page in pdf.pages:
                search_result = page.search(contents[page.page_number - 1], regex=False, case=True, return_chars=False,
                                            return_groups=False)
                print(search_result)
        search_result = pages[0].search(contents[0], regex=False, case=True, return_chars=False,
                                        return_groups=False)
        print("=========================\n")
        print(search_result)

    def test_extract2(self):
        contents = [
            "Column 2",
        ]
        path = os.path.join(os.path.dirname(__file__), "../examples", "pdfplumber_test.pdf")
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                search_result = page.search(contents[page.page_number - 1], regex=False, case=True)
                print(search_result)

    def test_image2pdf(self):
        image_path = os.path.join(os.path.dirname(__file__), "../examples", "digests-db.jpg")
        pdf_path = os.path.join(os.path.dirname(__file__), "../examples", "digests-db.pdf")
        with open(pdf_path, "wb") as f:
            f.write(img2pdf.convert([image_path]))
        # path = os.path.join(os.path.dirname(__file__), "examples", "K940242_ocr.pdf")
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                print(page.images)

    def test_ocr_pdf(self):
        pdf_path = os.path.join(os.path.dirname(__file__), "../examples", "ocr-parsed.pdf")
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                print(f"page number:{page.page_number}, content:{page.extract_text()}\n")

    def test_multi_columns_pdf(self):
        pdf_path = os.path.join(os.path.dirname(__file__), "../examples", "pdf-3.pdf")
        pages = [2]
        with pdfplumber.open(pdf_path, pages=pages,laparams={
            "line_overlap": 0.7
        }) as pdf:
            token = "in vivo expression of chemokine receptors in patients with allergic rhinitis [18]. Kinins are therefore potent mediators of inflammation, influencing vascular permeability, leukocyte ac- tivation, synthesis of neuropeptides, and the release of growth factors and eicosanoids [6, 11, 19]"
            #
            table_settings = {
                "horizontal_strategy": "text",
                "explicit_vertical_lines": True,
                "snap_tolerance": 0.005,
            }
            for page in pdf.pages:
                tables=page.extract_table(table_settings)

                left = page.crop((9, 9, 0.5 * float(page.width), page.height))
                # right = page.crop(
                #     (0.5 * float(page.width), 0.4 * float(page.height), page.width, 0.9 * float(page.height)))
                print(f"left:{left.extract_text()}")
                postions = page.search(token)
                print(f"postions: {postions}")
                lines = page.extract_text()
                print(f"lines: {lines}")
                # print(f"right:{right.extract_text()}")
    def test_extract2(self):
        pdf_path = os.path.join(os.path.dirname(__file__), "../examples", "71017.pdf")
        self.extractor.init_pdf(pdf_file=pdf_path)
        result: dict = self.extractor.extract_page()
        print(result.get('content'))
        for token in result.get('pages'):
            print(token)

        tokens = 'the association between eosinophils and kinins'
        positions = self.extractor.extract_position(page_number=7, token=tokens)
        for p in positions:
            print(json.dumps(p.__dict__))



