import os.path
import shutil
import unittest
from pdf_ocr_service.configula.pdf_ocr_config import OssConfig


class TestMinIO(unittest.TestCase):
    def setUp(self):
        host = 's3.amazonaws.com'
        port = 443
        access_key = "AKIAQQ3OKMH6W5RQFHFJ"
        secret_key = "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"
        secure = True
        region = 'us-east-2'

        self.oss = OssConfig(
            host=host,
            port=port,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure,
            region=region
        )

        self.bucket_name = 'dms-us-east2'

    def test_upload(self):
        file = '/Users/jinghuali/Desktop/PDF/archery-api.pdf'
        object_name = 'dev/pdf/unit-test/archery-api.pdf'
        try:
            result = self.oss.put_bucket_file(self.bucket_name, object_name=object_name, file_path=file)
            print(f"result={result}")
        except Exception as ex:
            print(f"error:{ex.args[0]}")

    def test_download(self):
        object_name = '/dev/pdf/ocr/43/V00001/K940261.pdf'
        tmp_dir = os.path.abspath(os.path.join(os.getcwd(), '../../', 'tmp'))
        try:
            result = self.oss.get_bucket_file(bucket_name=self.bucket_name, object_name=object_name,
                                              store_dir=tmp_dir,
                                              store_file_name='ocr-original.pdf'
                                              )
            print(f"result:{result}")
        except Exception as ex:
            print(f"occur error {ex.args[0]}")

    def test_join(self):
        path = os.path.join('/home', 'dd', 'ddd', 'a.txt')
        print(type(path))
        print(path)

    def test_dir(self):
        current_dir = os.getcwd()
        print("current_dir %s" % current_dir)
        tmp_dir = os.path.abspath(os.path.join(current_dir, '../../', 'tmp'))
        print('tmp_dir=[%s]' % tmp_dir)

    def test_rm_dir(self):
        tmp_dir = os.path.abspath(os.path.join(os.getcwd(), '../../', 'tmp'))
        if os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir)

    def test_exists(self):
        object_name = '/dev/pdf/ocr/43/V00001/K940261.pdf'
        exits = self.oss.exits(bucket_name=self.bucket_name, object_name=object_name)

        print(f" exits={exits}")
