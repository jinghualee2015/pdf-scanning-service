from celery.utils.log import get_logger

from pdf_ocr_service import TASK_LOG
from pdf_ocr_service.jobs.storage import BaseStorageService, get_storage_service

logger = logger = get_logger(TASK_LOG)


class DmsServiceConfig(object):
    def __init__(self,
                 schema=None,
                 host=None,
                 port=None,
                 headers=None,
                 path=None,
                 method='POST'
                 ):
        self.schema = schema
        self.host = host
        self.port = port
        self.headers = headers
        self.path = path
        self.method = method

    def get_url(self):
        path = f"{self.schema}://{self.host}:{self.port}{self.path}"
        return path

    def get_headers(self):
        return self.headers

    def get_method(self):
        return self.method


class OssConfig(object):
    def __init__(self,
                 host=None,
                 port=None,
                 access_key=None,
                 secret_key=None,
                 secure=False,
                 bucket_name=None,
                 region=None,
                 ):
        self.host = host
        self.port = port
        self.access_key = access_key
        self.secret_key = secret_key
        self.secure = secure
        self.bucket_name = bucket_name
        self.region = region
        logger.debug(
            f"host={host} , port={port}, access_key={access_key},  secret_key={secret_key}, bucket={bucket_name}, region={region}")
        self.client: BaseStorageService = get_storage_service(storage_type='s3',
                                                              host=self.host,
                                                              access_key=self.access_key,
                                                              secret_key=self.secret_key,
                                                              secure=self.secure,
                                                              region=self.region
                                                              )

    def get_oss_client(self) -> BaseStorageService:
        return self.client

    def put_bucket_file(self, bucket_name=None, object_name=None, file_path=None) -> str:
        self.client.put_bucket_file(bucket_name=bucket_name,
                                    object_name=object_name,
                                    file_path=file_path)

    def get_bucket_file(self, bucket_name=None, object_name=None, store_dir=None, store_file_name=None) -> str:
        return self.client.get_bucket_file(bucket_name=bucket_name,
                                           object_name=object_name,
                                           store_dir=store_dir,
                                           store_file_name=store_file_name)

    def exits(self, bucket_name=None, object_name=None):
        self.client.exits(bucket_name=bucket_name,
                          object_name=object_name)


class BaseAiModelInfo(object):
    def __init__(self, model_id: str = ''):
        self._model_id = model_id if model_id else ''

    @property
    def model_id(self):
        return self._model_id


class EmbeddingModelInfo(BaseAiModelInfo):
    def __init__(self, model_id: str = '', input_type: str = ''):
        super().__init__(model_id=model_id)
        self._input_type = input_type if input_type else ''

    @property
    def input_type(self):
        return self._input_type


class SummaryModelInfo(BaseAiModelInfo):
    def __init__(self, model_id: str = '',
                 max_tokens_to_sample: int = 1024,
                 temperature: float = 0.1,
                 stop_sequences: list = [],
                 ):
        super().__init__(model_id=model_id)
        self._max_tokens_to_sample = max_tokens_to_sample
        self._temperature = temperature
        self._stop_sequences = stop_sequences

    @property
    def max_tokens_to_sample(self):
        return self._max_tokens_to_sample

    @property
    def stop_sequences(self):
        return self._stop_sequences

    @property
    def temperature(self):
        return self._temperature


class AiConfig(object):
    def __init__(self,
                 access_key: str = '',
                 secret_key: str = '',
                 service_name: str = '',
                 accept: str = 'application/json',
                 content_type: str = 'application/json',
                 region_name: str = '',
                 embedding: EmbeddingModelInfo = None,
                 summary: SummaryModelInfo = None,
                 ):
        self._access_key = access_key
        self._secret_key = secret_key
        self._service_name = service_name
        self._accept = accept
        self._region_name = region_name
        self._content_type = content_type
        self._embedding = embedding
        self._summary = summary

    @property
    def access_key(self):
        return self._access_key

    @property
    def secret_key(self):
        return self._secret_key

    @property
    def service_name(self):
        return self._service_name

    @property
    def accept(self):
        return self._accept

    @property
    def region_name(self):
        return self._region_name

    @property
    def content_type(self):
        return self._content_type

    @property
    def embedding_info(self) -> EmbeddingModelInfo:
        return self._embedding

    @property
    def summary_info(self) -> SummaryModelInfo:
        return self._summary


class PdfOcrConfig(object):
    def __init__(self,
                 main_config: dict = None,
                 oss_cfg: OssConfig = None,
                 dms_cfg: DmsServiceConfig = None,
                 ai_cfg: AiConfig = None,
                 ):
        self.tmp_pdf_path = main_config.get('tmp_pdf_path')
        self.app_name = main_config.get('app_name')
        self.default_language = main_config.get('default_language')
        self.oss_cfg: OssConfig = oss_cfg
        self.dms_cfg: DmsServiceConfig = dms_cfg
        self.ai_config = ai_cfg
