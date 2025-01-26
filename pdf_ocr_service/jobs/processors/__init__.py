"""
document processors package
"""
__version__ = '1.0.0'
__autor__ = 'NyquistAI technique team'
__maintainer__ = 'James Lee'
__contact__ = 'china_tech@nyquistdata.com'
__homepage__ = 'https://nyquistai.com'
__docformat__ = 'restructuredtext'

from .pdf_ocr_task_processor import PdOcrfTaskProcessor
from .image_identification_task_processor import ImageIdentifyTaskProcessor
from .office_extract_task_processor import OfficeExtractTaskProcessor
from .pdf_extract_task_processor import PdfExtractTaskProcessor

__all__ = (
    "PdOcrfTaskProcessor",
    "OfficeExtractTaskProcessor",
    "ImageIdentifyTaskProcessor",
    "PdfExtractTaskProcessor"
)
