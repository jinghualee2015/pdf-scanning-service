import unittest
from pdf_ocr_service.celery import task_logger
from pdf_ocr_service.celery import worker_logger

tsk_logger = task_logger
test_logger = worker_logger


class LogTest(unittest.TestCase):

    def test_01(self):
        tsk_logger.info("[TASK Logger]This is celery log test....")
        test_logger.info("[Worker Logger]This is celery log test....")
