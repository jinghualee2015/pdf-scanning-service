"""
task data transfer object package
"""
__version__ = '1.0.0'
__autor__ = 'NyquistAI technique team'
__maintainer__ = 'James Lee'
__contact__ = 'china_tech@nyquistdata.com'
__homepage__ = 'https://nyquistai.com'
__docformat__ = 'restructuredtext'

from .document_process_result import DocumentProcessResult
from .document_task_info import DocumentTaskInfo
from .document_pdf_task_info import DocumentPdfOcrTaskInfo, DocumentPdfExtractTaskInfo
from .document_office_task_info import DocumentOfficeTaskInfo
from .document_image_task_info import DocumentImageTaskInfo
from .document_embedding_token import EmbeddingToken
from .token_postion import TokenPosition

__all__ = (
    "DocumentProcessResult",
    "DocumentTaskInfo",
    "DocumentPdfOcrTaskInfo",
    "DocumentPdfExtractTaskInfo",
    "DocumentOfficeTaskInfo",
    "DocumentImageTaskInfo",
    "EmbeddingToken",
    "TokenPosition"
)
