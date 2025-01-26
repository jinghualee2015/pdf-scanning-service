"""
database operate  package
"""
__version__ = '1.0.0'
__autor__ = 'NyquistAI technique team'
__maintainer__ = 'James Lee'
__contact__ = 'china_tech@nyquistdata.com'
__homepage__ = 'https://nyquistai.com'
__docformat__ = 'restructuredtext'

from pdf_ocr_service.jobs.db.models import (DmsDocuments, DmsDocumentVersions, DmsDocumentsProcessTasks,
                                            DmsDocumentEmbedding)
from pdf_ocr_service.jobs.db.db_utils import update_process_content, update_ocr_result

__all__ = (
    "DmsDocuments",
    "DmsDocumentVersions",
    "DmsDocumentsProcessTasks",
    "DmsDocumentEmbedding",
    "update_process_content",
    "update_ocr_result"
)
