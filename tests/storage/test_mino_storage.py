import os
import unittest
from pdf_ocr_service.jobs.storage import get_storage_service, BaseStorageService


class StorageServiceTest(unittest.TestCase):
    def setUp(self):
        self.host = 's3.amazonaws.com'
        self.port = 443
        self.access_key = "AKIAQQ3OKMH6W5RQFHFJ"
        self.secret_key = "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"
        self.secure = True
        self.region = 'us-east-2'
        self.bucket_name = 'dms-us-east2'
        self.client: BaseStorageService = get_storage_service(storage_type='mino',
                                                              host=self.host,
                                                              access_key=self.access_key,
                                                              secret_key=self.secret_key,
                                                              secure=self.secure,
                                                              region=self.region
                                                              )

    def test_upload(self):
        file = os.path.join(os.path.dirname(__file__), "../examples", "K940242_ocr.pdf")
        object_name = 'dev/pdf/unit-test/K940242_ocr.pdf'
        try:
            result = self.client.put_bucket_file(self.bucket_name, object_name=object_name, file_path=file)
            print(f"result={result}")
        except Exception as ex:
            print(f"error:{ex.args[0]}")

    def test_download(self):
        object_name = 'dev/pdf/unit-test/K940242_ocr.pdf'
        tmp_dir = os.path.abspath(os.path.join(os.getcwd(), '../../', 'tmp'))
        try:
            result = self.client.get_bucket_file(bucket_name=self.bucket_name,
                                                 object_name=object_name,
                                                 store_dir=tmp_dir,
                                                 store_file_name='ocr-original.pdf'
                                                 )
            print(f"result:{result}")
        except Exception as ex:
            print(f"occur error {ex.args[0]}")

    def test_exits(self):
        result = self.client.exits(self.bucket_name, 'dev/pdf/unit-test/K940242_ocr.pdf')
        print(f'exist:{result}')

        result = self.client.exits(self.bucket_name, 'xxxxx')
        print(f'exist:{result}')
