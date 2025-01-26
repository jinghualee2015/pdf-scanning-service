import json
import os
import time
import ocrmypdf
import requests

from pdf_ocr_service.factory.app_factory import service_config

from pdf_ocr_service.jobs.domains import DocumentPdfOcrTaskInfo
from pdf_ocr_service.jobs.processors.base_processor import BaseDocumentProcessor
from pdf_ocr_service.jobs.extractors import OcrPyMupdfExtractor
from pdf_ocr_service.jobs.db import update_ocr_result

from pdf_ocr_service.celery import task_logger

logger = task_logger


class PdOcrfTaskProcessor(BaseDocumentProcessor):
    def __init__(self, task_info: DocumentPdfOcrTaskInfo = None):
        super(PdOcrfTaskProcessor, self).__init__(task_info=task_info)
        self.return_data = dict(
            message="OK",
            code=200,
            params=self.task_info.task_params,
            result=dict(
                process_file_path=self.task_info.store_ocr_file_name,
                side_car_file_path=self.task_info.store_ocr_sidecar_name,
            )
        )
        self.process_result.set_file_path(self.task_info.store_ocr_file_name)
        self.process_result.set_side_car_path(self.task_info.store_ocr_sidecar_name)
        self.extractor = None
        self.extractor = OcrPyMupdfExtractor()
        self.extractor.init_side_car_path(self.task_info.tmp_ocr_sidecar_dir)

    def business_process(self):
        try:
            self.pull_source_pdf()
            self.ocr_pdf()
            self.push_ocr_file()
        except Exception as e:
            self.return_data['code'] = 500
            self.return_data['message'] = ",".join(str(i) for i in e.args)
            self.return_data['result'] = dict(
                process_file_path='',
                side_car_file_path='',
            )
            self.process_result.set_status(False)
            self.process_result.set_error_msg(self.return_data['message'])
        finally:
            self.generate_summary()
            self.generate_tokens()
            self.notify_result_to_db()
            self.clear_tmp_file()

    def ocr_pdf(self) -> dict:
        logger.info(f"begin ocr document:[{self.task_info.document_id}] pdf file...")
        start_time = time.time()
        tmp_input = os.path.join(self.task_info.tmp_dir, self.task_info.tmp_source_file_name)
        try:
            ocrmypdf.ocr(
                input_file=tmp_input,
                output_file=self.task_info.tmp_ocr_file_name,
                plugins=["pdf_ocr_service.plugins.ocr.plugin"],
                # lang=self.task_info.language,
                force_ocr=True,
                progress_bar=False,
                output_type="pdf",
                use_threads=True,
                keep_temporary_files=False,
                sidecar=self.task_info.tmp_ocr_sidecar_name,
                deskew=True,
                sidecar_dir=self.task_info.tmp_ocr_sidecar_dir,
            )
            self.process_result.set_file_path(self.task_info.store_ocr_file_name)
            self.process_result.set_side_car_path(self.task_info.store_ocr_sidecar_name)
            self.read_content()
        except Exception as ex:
            import traceback
            error = traceback.format_exc()
            logger.error(f"ocr pdf:{tmp_input}\n occur error:{error}")
            self.process_result.set_file_path('')
            self.process_result.set_side_car_path('')
            raise Exception(error)
        finally:
            end_time = time.time()
            logger.info(
                f"finish ocr document:[{self.task_info.document_id}] use time:[{end_time - start_time}] seconds")
        return dict(
            ocr_file=self.task_info.tmp_ocr_file_name,
            sider_car_file=self.task_info.tmp_ocr_sidecar_name
        )

    def push_ocr_file(self):
        logger.info(f"begin push ocr document:[{self.task_info.document_id}]....")
        service_config.oss_cfg.put_bucket_file(bucket_name=self.bucket_name,
                                               object_name=self.task_info.store_ocr_file_name,
                                               file_path=self.task_info.tmp_ocr_file_name
                                               )
        logger.info(f"complete push document:[{self.task_info.document_id}] ocr file")

    def notify_result_to_db(self):
        """
        update ocr result through db
        :return:
        """
        update_ocr_result(self.process_result)
        return True

    def read_content(self):
        self._extract()

    def _extract(self):
        logger.info(f"begin extract document:[{self.task_info.document_id}] pdf file ...")
        start_time = time.time()
        tmp_input = self.task_info.tmp_ocr_file_name
        try:
            self.extract_pages(tmp_input)
        except Exception as ex:
            import traceback
            error = traceback.format_exc()
            logger.error(f"extract pdf:{tmp_input}\n occur error:{error}")
            raise Exception(error)
        finally:
            end_time = time.time()
            logger.info(
                f"finish extract document:[{self.task_info.document_id}] use time:[{end_time - start_time}] seconds")

    def _push_target_files(self):
        logger.info(f"begin push ocr document:[{self.task_info.document_id}]....")
        service_config.oss_cfg.put_bucket_file(bucket_name=self.bucket_name,
                                               object_name=self.task_info.store_ocr_file_name,
                                               file_path=self.task_info.tmp_ocr_file_name
                                               )
        logger.info(f"complete push document:[{self.task_info.document_id}] ocr file")

        service_config.oss_cfg.put_bucket_file(bucket_name=self.bucket_name,
                                               object_name=self.task_info.store_ocr_sidecar_name,
                                               file_path=self.task_info.tmp_ocr_sidecar_name
                                               )
        logger.info(f"complete push document:[{self.task_info.document_id}] side-car file")
        logger.info(f"finish push ocr document:[{self.task_info.document_id}]....")

    def _notify_result(self):
        headers = service_config.dms_cfg.headers
        service_url = service_config.dms_cfg.get_url()
        method = service_config.dms_cfg.method
        body_data = json.dumps(self.return_data)
        logger.info(
            f"begin notify ocr document:[{self.task_info.document_id}] result to url= {service_config.dms_cfg.get_url()}\n "
            f"method=[{method}] \n"
            f"headers=[{headers}] \n"
            f"body=[{body_data}]")
        try:
            if 'POST' == method:
                result = requests.post(url=service_url, data=body_data, headers=headers)
            else:
                result = requests.get(url=service_url, data=body_data, headers=headers)
            logger.info(
                f"finish notify ocr document:[{self.task_info.document_id}] result to {service_config.dms_cfg.get_url()} \n"
                f"get feed_back:[{result.json()}] .")
            result.close()
        except Exception as err:
            logger.error(f"notify result occur error:{err.args[0]}")
