import logging
import traceback
import unittest

import requests


class TestRequest(unittest.TestCase):
    def test_request1(self):
        for i in range(1, 200):
            result = requests.post(url='https://www.baidu.com')
            print(result.text)
            result.close()

    def test_str_ex(self):
        try:
            1 / 0
        except Exception as ex:
            error_msg = str(ex)
            # logging.error(f"occur error:{error_msg}")
            logging.error(f"trace_book:{traceback.format_exc()}")
            logging.error(f" print: {traceback.print_exc()}")
