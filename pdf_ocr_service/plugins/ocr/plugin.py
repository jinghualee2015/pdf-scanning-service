from pathlib import Path

from ocrmypdf import hookimpl
from ocrmypdf._exec import tesseract

from ocrmypdf.builtin_plugins.tesseract_ocr import TesseractOcrEngine
from .extract_text_utils import copy_text


class CustomEngine(TesseractOcrEngine):
    @staticmethod
    def generate_pdf(input_file, output_pdf, output_text, options):
        tesseract.generate_pdf(
            input_file=input_file,
            output_pdf=output_pdf,
            output_text=output_text,
            languages=options.languages,
            engine_mode=options.tesseract_oem,
            tessconfig=options.tesseract_config,
            timeout=options.tesseract_timeout,
            pagesegmode=options.tesseract_pagesegmode,
            user_words=options.user_words,
            user_patterns=options.user_patterns,
            thresholding=options.tesseract_thresholding
        )
        copy_text(
            input_file_path=Path(output_text),
            output_dir=options.sidecar_dir
        )


@hookimpl
def get_ocr_engine():
    return CustomEngine()


@hookimpl
def add_options(parser):
    parser.add_argument(
        '--sidecar-dir',
        help="Folder where to write generated files"
    )
