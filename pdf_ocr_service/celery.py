import os

from pdf_ocr_service import WORKER_LOG
from pdf_ocr_service import TASK_LOG
from pdf_ocr_service.factory.app_factory import get_celery
from celery.utils.log import get_logger

task_logger = get_logger(TASK_LOG)
worker_logger = get_logger(WORKER_LOG)
app = get_celery()
config_file = os.environ.get('CONFIG_FILE')
if config_file is not None:
    worker_logger.debug(f"Load config file:{config_file}")
worker_logger.debug(f"app config:{app.conf}")
worker_logger.info("pdf-ocr-service task running....")
