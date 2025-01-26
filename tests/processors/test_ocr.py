import os
import unittest
import uuid
from pathlib import Path
from tempfile import gettempdir

import ocrmypdf
import pdfplumber


class OcrTest(unittest.TestCase):
    def setUp(self):
        self.tmp_input = os.path.join(os.path.dirname(__file__), "../examples", "demo-ocr.pdf")
        self.output_file = os.path.join(os.path.dirname(__file__), "../examples", "ocr-parsed.pdf")
        self.keep_temporary_files = True
        self.sidecard_name = os.path.join(os.path.dirname(__file__), "../examples", "ocr-sidecar.txt")

    def test_01(self):
        result = ocrmypdf.ocr(
            input_file=self.tmp_input,
            output_file=self.output_file,
            # lang=self.task_info.language,
            force_ocr=True,
            progress_bar=False,
            output_type="pdf",
            use_threads=True,
            keep_temporary_files=self.keep_temporary_files,
            sidecar=self.sidecard_name,
            deskew=True
        )
        print(result)
        tmp_dir = gettempdir()
        print(tmp_dir)

    def test_pdf_check(self):
        path = "/Users/jinghuali/Downloads/pdf-to-check"
        target_path = os.path.join(os.path.dirname(__file__), '../examples', 'ocr')
        for file_name in os.listdir(path):
            print(f"process {file_name} begin...........\n")
            name = file_name.split(".")[0]
            original_file_name = os.path.join(path, file_name)
            ocr_pdf_name = os.path.join(target_path, name + "_ocr.pdf")
            sidecar_name = os.path.join(target_path, name + ".txt")
            ocrmypdf.ocr(
                input_file=original_file_name,
                output_file=ocr_pdf_name,
                force_ocr=True,
                progress_bar=False,
                output_type="pdf",
                use_threads=True,
                keep_temporary_files=False,
                sidecar=sidecar_name,
                deskew=True
            )
            with pdfplumber.open(ocr_pdf_name) as pdf:
                for page in pdf.pages:
                    print(f"page number:{page.page_number}, content:{page.extract_text()}\n")

            print(f"process {file_name} end...........\n")

    def test_text_extract(self):
        path = "/Users/jinghuali/Downloads/pdf-to-check"
        tmp_input = path + '/71017.pdf'
        out_put_path = os.path.join(path, '71017', 'ocred')
        side_car_path = os.path.join(path, '71017', 'sidecars')
        target_path = Path(out_put_path)
        if not target_path.exists():
            os.makedirs(
                target_path,
                exist_ok=True
            )

        output_file = out_put_path + '/71007.pdf'
        target_path = Path(side_car_path)
        if not target_path.exists():
            os.makedirs(
                side_car_path,
                exist_ok=True
            )

        print(f"output_path={out_put_path}, sidecars={side_car_path}, output_file={output_file}")
        ocrmypdf.ocr(
            input_file=tmp_input,
            output_file=output_file,
            plugins=["pdf_ocr_service.plugins.ocr.plugin"],
            # lang=self.task_info.language,
            force_ocr=True,
            progress_bar=False,
            output_type="pdf",
            use_threads=True,
            keep_temporary_files=False,
            sidecar_dir=side_car_path,
        )

        pages: list[dict] = []
        files = os.listdir(side_car_path)
        sorted_files = sorted(files, key=lambda name: int(name.split(".")[0]))
        for page_number, file in enumerate(sorted_files):
            text_path = f"{side_car_path}/{file}"
            with open(text_path, 'r') as page_file:
                content = page_file.read()
                pages.append({
                    'content': content,
                    'page': page_number
                })

        print(pages)

    def test_spilit(self):
        file = '29.txt'
        names = file.split(".")
        print(names)
