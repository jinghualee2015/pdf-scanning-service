import os
import unittest

from fitz import fitz

from pdf_ocr_service.jobs.extractors import OcrPyMupdfExtractor


class OcrPyMupdfExtractorTest(unittest.TestCase):
    def test_extract(self):
        pdf_name = '71017'
        path = "/Users/jinghuali/Downloads/pdf-to-check"
        tmp_input = path + f'/{pdf_name}.pdf'
        out_put_path = os.path.join(path, pdf_name, 'ocred')
        side_car_path = os.path.join(path, pdf_name, 'sidecars')
        output_file = out_put_path + f'/{pdf_name}.pdf'
        extractor = OcrPyMupdfExtractor(
        )
        extractor.init_side_car_path(side_car_path=side_car_path)
        extractor.init_pdf(output_file)
        result = extractor.extract_page()
        token = """CENTER For Druc EVALUATION AND RESEARCH

Guidance for Industry

The FDA published Good Guidance Practices in February 1997.
This guidance was developed and issued prior to that date.

Additional copies are available from:
Office of Training and Communications
Division of Communications Management

Drug Information Branch, HFD-210

5600 Fishers Lane
Rockville, MD 20857

(Tel) 301-827-4573
(Internet) http://www.fda. gov/cder/guidance/index.htm

U.S. DreparTMENT OF HEALTH AND HuMAN SERVICES, FOOD AND DruG ADMINISTRATION"""
        lines = token.split("\n")
        page = extractor.pdf_obj.load_page(0)
        for line in lines:
            line = line.strip()
            if line == '':
                continue
            text_instances = page.search_for(line, flags=fitz.TEXTFLAGS_TEXT)
            for inst in text_instances:
                page.add_highlight_annot(inst)

        extractor.pdf_obj.save(os.path.join(os.path.dirname(__file__), "../examples", f"{pdf_name}-positions.pdf"),
                               garbage=4,
                               deflate=True,
                               clean=True)
