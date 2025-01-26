import os
import time
import ocrmypdf

from pdf_ocr_service.factory.app_factory import service_config

from pdf_ocr_service.jobs.domains import DocumentImageTaskInfo
from pdf_ocr_service.jobs.processors.base_processor import BaseDocumentProcessor

from pdf_ocr_service.celery import task_logger

logger = task_logger


class ImageIdentifyTaskProcessor(BaseDocumentProcessor):
    def __init__(self, task_info: DocumentImageTaskInfo = None):
        super(ImageIdentifyTaskProcessor, self).__init__(task_info=task_info)

    def business_process(self):
        try:
            self.pull_source_pdf()
            self.image_to_pdf()
            self.ocr_pdf()
            self.push_target_files()
        except Exception as e:
            message = ",".join(str(i) for i in e.args)
            self.process_result.set_status(False)
            self.process_result.set_error_msg(message)
        finally:
            self.notify_result()
            self.clear_tmp_file()

    def image_to_pdf(self):
        pass

    def ocr_pdf(self) -> dict:
        logger.info(f"begin ocr document:[{self.task_info.document_id}] pdf file...")
        start_time = time.time()
        tmp_input = os.path.join(self.task_info.tmp_dir, self.task_info.tmp_source_file_name)
        try:
            ocrmypdf.ocr(
                input_file=tmp_input,
                output_file=self.task_info.tmp_ocr_file_name,
                lang=self.task_info.language,
                force_ocr=True,
                progress_bar=False,
                output_type="pdf",
                use_threads=True,
                keep_temporary_files=False,
                sidecar=self.task_info.tmp_ocr_sidecar_name,
                deskew=True
            )
        except Exception as ex:
            import traceback
            error = traceback.format_exc()
            logger.error(f"ocr pdf:{tmp_input}\n occur error:{error}")
            raise Exception(error)
        finally:
            self.process_result.set_file_path(self.task_info.tmp_ocr_file_name)
            self.process_result.set_side_car_path(self.task_info.tmp_ocr_sidecar_name)
            self.read_content()
            end_time = time.time()
            logger.info(
                f"finish ocr document:[{self.task_info.document_id}] use time:[{end_time - start_time}] seconds")
        return dict(
            ocr_file=self.task_info.tmp_ocr_file_name,
            sider_car_file=self.task_info.tmp_ocr_sidecar_name
        )

    def push_target_files(self):
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

    def read_content(self):
        if not os.path.exists(self.task_info.tmp_ocr_sidecar_name):
            logger.warn(f"due to side car file not exits, just set content as empty")
            self.process_result.set_content('')
        content: str = ''
        with open(self.task_info.tmp_ocr_sidecar_name) as sidecar:
            for line in sidecar.readlines():
                line.strip()
                content += line
        self.process_result.set_content(content)
