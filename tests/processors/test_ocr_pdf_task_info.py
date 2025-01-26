import unittest

from pdf_ocr_service.jobs.domains import DocumentPdfOcrTaskInfo


class DomainTest(unittest.TestCase):
    def test_ocr_domain(self):
        task_params = {'bucket_name': 'dms-us-east2',
                       'tmp_dir': './tmp',
                       'document_id': '2245',
                       'language': 'eng',
                       # 'max_retries': 0,
                       # 'queue_name': 'pdf_ocr',
                       # 'retry': 0,
                       'source_file': 'dev/pdf/extract/2245/V00001/original/71876.pdf',
                       'target_file_name': '71876.pdf',
                       'target_path': 'dev/pdf/ocr2245/V00001/',
                       'task_id': '87-93a54727fac54e36b3dbe29fb6dca2ca',
                       # 'task_key': 'ocrPdf',
                       # 'task_name': 'pdf_ocr_service.jobs.tasks.ocr_pdf_document',
                       'version': 1}

        task: DocumentPdfOcrTaskInfo = DocumentPdfOcrTaskInfo(task_params=task_params, **task_params)
        print(task.target_file_name)
        print(task.store_ocr_file_name)
