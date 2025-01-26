import json
import os

from pdf_ocr_service.jobs.domains.document_task_info import DocumentTaskInfo


class DocumentImageTaskInfo(DocumentTaskInfo):
    """
    Pdf type document ocr task information
    """

    def __init__(self,
                 task_params: dict = None,
                 document_id: int = None,
                 task_id: str = None,
                 version: int = None,
                 source_file: str = None,
                 language: str = None,
                 target_path: str = None,
                 target_file_name: str = None,
                 tmp_dir: str = None,
                 bucket_name: str = None,
                 ):
        super(DocumentImageTaskInfo, self).__init__(
            task_params=task_params,
            document_id=document_id,
            task_id=task_id,
            version=version,
            source_file=source_file,
            language=language,
            target_path=target_path,
            tmp_dir=tmp_dir,
            bucket_name=bucket_name
        )
        self.tmp_source_file_name = f"{document_id}.pdf"
        self.tmp_ocr_file_name = os.path.join(self.tmp_dir, f"{document_id}-ocr.pdf")
        self.tmp_ocr_sidecar_name = os.path.join(self.tmp_dir, f"{document_id}-ocr-sidecar.txt")
        self.store_ocr_file_name = os.path.join(self.target_path, f"{target_file_name}.pdf")
        self.store_ocr_sidecar_name = os.path.join(self.target_path, f"{target_file_name}.txt")

    def __str__(self):
        return json.dumps(self)

    @property
    def get_target_pdf_file(self):
        return os.path.join(self.target_path, self.target_file_name + '.pdf')

    @property
    def get_target_text_file(self):
        return os.path.join(self.target_path, self.target_file_name + '.txt')
