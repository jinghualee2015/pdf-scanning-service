import os

from minio import Minio
from celery.utils.log import get_logger

from pdf_ocr_service.jobs.storage import BaseStorageService

logger = logger = get_logger("mino-storage-service")


class MinIOStorageService(BaseStorageService):
    def __init__(self,
                 host=None,
                 access_key=None,
                 secret_key=None,
                 secure=False,
                 region=None,
                 ):
        self.client = Minio(
            endpoint=host,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure,
            region=region)

    def put_bucket_file(self, bucket_name=None, object_name=None, file_path=None) -> str:
        logger.info(f"put_bucket_file object_name:[{object_name}] file_path:[{file_path}]")
        try:
            result = self.client.fput_object(bucket_name=bucket_name, object_name=object_name, file_path=file_path)
            return result.object_name
        except Exception as ex:
            logger.error(f"check exits occur error:{ex.args[0]}")

    def get_bucket_file(self, bucket_name=None, object_name=None, store_dir=None, store_file_name=None) -> str:
        file_data = self.client.get_object(bucket_name=bucket_name, object_name=object_name)
        if not os.path.exists(store_dir):
            os.makedirs(store_dir)
        file_name = os.path.join(store_dir, store_file_name)
        logger.info(f"get buck file object_name:[{object_name}] local_file_name:[{file_name}]")
        with open(file_name, 'wb') as target_file:
            for d in file_data.stream(32 * 1024):
                target_file.write(d)
        return file_name

    def exits(self, bucket_name=None, object_name=None):
        if object_name is None or object_name == '':
            return False
        prefix = object_name[1:len(object_name) - 1]
        try:
            objects = self.client.list_objects(bucket_name=bucket_name, prefix=prefix)
            for _ in objects:
                return True
        except Exception as ex:
            logger.error(f"check exits occur error:{ex.args[0]}")
            return False
