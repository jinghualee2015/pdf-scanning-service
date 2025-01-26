from abc import ABCMeta, abstractmethod


class BaseStorageService(metaclass=ABCMeta):
    @abstractmethod
    def put_bucket_file(self, bucket_name=None, object_name=None, file_path=None) -> str:
        """
        put local file to remote storage
        :param bucket_name:  storage bucket name
        :param object_name: store in storage file name
        :param file_path: local file path
        :return: remote storage file path
        """
        pass

    @abstractmethod
    def get_bucket_file(self, bucket_name=None, object_name=None, store_dir=None, store_file_name=None) -> str:
        """
        get file from remote storage and store in local file system
        :param bucket_name: storage's bucket name
        :param object_name: storage's file path
        :param store_dir: local file system path
        :param store_file_name: file name in local file system
        :return: local file path
        """
        pass

    @abstractmethod
    def exits(self, bucket_name=None, object_name=None):
        """
        check the target object whether exist or not
        :param bucket_name: storage's bucket name
        :param object_name: storage's object name
        :return: true means exits otherwise not exits
        """
        pass
