"""
pdf document extractor package
"""
__version__ = '1.0.0'
__autor__ = 'NyquistAI technique team'
__maintainer__ = 'James Lee'
__contact__ = 'china_tech@nyquistdata.com'
__homepage__ = 'https://nyquistai.com'
__docformat__ = 'restructuredtext'

from .base_pdf_extractor import BasePdfExtractor
from .pypdf_extractor import PyPdfExtractor
from .pymupdf_extractor import PyMupdfExtractor
from .pdfplumber_extractor import PdfPlumberExtractor
from .composite_pdf_extractor import CompositePdfExtractor
from .ocr_pymupdf_extractor import OcrPyMupdfExtractor

__all__ = (
    "BasePdfExtractor",
    "PdfPlumberExtractor",
    "PyMupdfExtractor",
    "PyPdfExtractor",
    "CompositePdfExtractor",
    "OcrPyMupdfExtractor"
)
