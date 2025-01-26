
class DocumentTaskInfo(object):
    """

    Base Document Task Class
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
        self.task_params = task_params
        self.document_id = document_id
        self.task_id = task_id
        self.version = version
        self.source_file = source_file
        self.language = language if language is not None else 'eng'
        self.target_path = target_path
        self.target_file_name = target_file_name
        self.tmp_dir = tmp_dir
        self.bucket_name = bucket_name
