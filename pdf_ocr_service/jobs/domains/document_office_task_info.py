from pdf_ocr_service.jobs.domains.document_task_info import DocumentTaskInfo


class DocumentOfficeTaskInfo(DocumentTaskInfo):
    """
    Office type document extract task information
    """

    def __init__(self,
                 task_params: dict = None,
                 document_id: int = None,
                 task_id: str = None,
                 version: int = None,
                 source_file: str = None,
                 language: str = None,
                 target_path: str = None,
                 tmp_dir: str = None,
                 bucket_name: str = None,
                 ):
        super(DocumentOfficeTaskInfo, self).__init__(
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
        self.tmp_source_file_name = f"{document_id}-{version}.pdf"
