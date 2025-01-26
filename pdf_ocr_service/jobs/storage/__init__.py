"""
document storage package
"""
__version__ = '1.0.0'
__autor__ = 'NyquistAI technique team'
__maintainer__ = 'James Lee'
__contact__ = 'china_tech@nyquistdata.com'
__homepage__ = 'https://nyquistai.com'
__docformat__ = 'restructuredtext'

from .base_storage_service import BaseStorageService
from .minio_storage_service import MinIOStorageService
from .s3_storage_service import S3StorageService

__all__ = (
    "BaseStorageService",
    "S3StorageService",
    "S3StorageService",
    "get_storage_service"
)


def get_storage_service(
        storage_type: str = 's3',
        host: str = None,
        access_key: str = None,
        secret_key: str = None,
        secure: bool = False,
        region: str = None) -> BaseStorageService:
    """
    get storage service instance
    :param region: storage region
    :param secret_key: access secret
    :param secure: whether use https
    :param access_key: access key
    :param host: storage host information
    :arg storage_type storage client type default is s3
    :return: BaseStorageService instance
    """

    if 's3' == storage_type:
        return S3StorageService(access_key=access_key, secret_key=secret_key, region=region)
    else:
        return MinIOStorageService(host=host, access_key=access_key, secret_key=secret_key, secure=secure,
                                   region=region)
