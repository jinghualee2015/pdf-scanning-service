import os

from botocore.exceptions import ClientError
from celery.utils.log import get_logger
import boto3
from pdf_ocr_service.jobs.storage import BaseStorageService

logger = logger = get_logger("s3-storage-service")


class S3StorageService(BaseStorageService):
    def __init__(self,
                 access_key=None,
                 secret_key=None,
                 region=None):
        self.client = boto3.client(service_name='s3',
                                   aws_access_key_id=access_key,
                                   aws_secret_access_key=secret_key,
                                   region_name=region)

    def put_bucket_file(self, bucket_name=None, object_name=None, file_path=None) -> str:
        logger.info(f"put_bucket_file object_name:[{object_name}] file_path:[{file_path}]")
        try:
            with open(file_path, "rb") as file:
                self.client.upload_fileobj(file, bucket_name, object_name)
                return object_name
        except Exception as ex:
            logger.error(f"check exits occur error:{ex.args[0]}")
            return ''

    def get_bucket_file(self, bucket_name=None, object_name=None, store_dir=None, store_file_name=None) -> str:

        if not os.path.exists(store_dir):
            os.makedirs(store_dir)
        file_name = os.path.join(store_dir, store_file_name)
        logger.info(f"get buck file object_name:[{object_name}] local_file_name:[{file_name}]")
        with open(file_name, 'wb') as target_file:
            self.client.download_fileobj(bucket_name, object_name, target_file)
        return file_name

    def exits(self, bucket_name=None, object_name=None):
        try:
            self.client.head_object(Bucket=bucket_name, Key=object_name)
        except ClientError as e:
            if e.response['Error']['Code'] == '403':
                return False
        else:
            return True
