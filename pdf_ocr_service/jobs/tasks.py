"""
Celery 分布式任务
"""
import os
from pdf_ocr_service.celery import app, task_logger
from pdf_ocr_service.factory.app_factory import service_config
from pdf_ocr_service.jobs.domains import DocumentPdfExtractTaskInfo, DocumentOfficeTaskInfo, DocumentPdfOcrTaskInfo
from pdf_ocr_service.jobs.processors import PdOcrfTaskProcessor, OfficeExtractTaskProcessor, PdfExtractTaskProcessor

logger = task_logger


@app.task
def ocr_pdf_document(task_dict: dict):
    """
    process pdf type document, ocr pdf document and upload
    parsed document to oss
    :return: None
    """
    logger.info(f"ocr_pdf_document receive task info:{task_dict}")
    tmp_dir = __get_tmp_dir(task_dict)
    task_info = DocumentPdfOcrTaskInfo(
        task_params=task_dict,
        document_id=task_dict.get('document_id'),
        task_id=task_dict.get('task_id'),
        version=task_dict.get('version'),
        source_file=task_dict.get('source_file'),
        language=task_dict.get('language'),
        target_path=task_dict.get('target_path'),
        target_file_name=task_dict.get('target_file_name'),
        tmp_dir=tmp_dir,
        bucket_name=task_dict.get('bucket_name'),
    )
    processor = PdOcrfTaskProcessor(task_info=task_info)
    processor.process()


@app.task
def identify_image_document(task_dict: dict):
    """
    process image document data
    :param task_dict: job data
    :return: None
    """
    logger.info(f"identify_image_document receive task info:{task_dict}")


@app.task
def extract_office_document(task_dict: dict):
    """
    process office document, just extract data
    :param task_dict:
    :return:
    """
    logger.info(f"extract_office_document receive task info:{task_dict}")
    tmp_dir = __get_tmp_dir(task_dict)
    task_info = DocumentOfficeTaskInfo(
        task_params=task_dict,
        document_id=task_dict.get('document_id'),
        task_id=task_dict.get('task_id'),
        version=task_dict.get('version'),
        source_file=task_dict.get('source_file'),
        language=task_dict.get('language'),
        target_path=task_dict.get('target_path'),
        tmp_dir=tmp_dir,
        bucket_name=task_dict.get('bucket_name'),
    )
    processor = OfficeExtractTaskProcessor(task_info=task_info)
    processor.process()


@app.task
def extract_pdf_document(task_dict: dict):
    """
    extract pdf data
    :param task_dict: task info
    :return: process result
    """
    logger.info(f"extract_pdf_document receive task info:{task_dict}")
    tmp_dir = __get_tmp_dir(task_dict)
    task_info = DocumentPdfExtractTaskInfo(
        task_params=task_dict,
        document_id=task_dict.get('document_id'),
        task_id=task_dict.get('task_id'),
        version=task_dict.get('version'),
        source_file=task_dict.get('source_file'),
        language=task_dict.get('language'),
        target_path=task_dict.get('target_path'),
        tmp_dir=tmp_dir,
        bucket_name=task_dict.get('bucket_name'),
    )
    processor = PdfExtractTaskProcessor(task_info=task_info)
    processor.process()


def __get_tmp_dir(task_dict: dict) -> dict:
    task_id = task_dict.get('task_id')
    tmp_dir = os.path.join(service_config.tmp_pdf_path, task_id)
    return tmp_dir
