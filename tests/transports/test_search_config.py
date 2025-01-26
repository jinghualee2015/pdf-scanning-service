import json
import os
import unittest

from pdf_ocr_service.configula import Configula


class TestServiceConfig(unittest.TestCase):
    def setUp(self):
        self.toml_file = os.path.join(
            os.path.dirname(__file__), "../examples", "pdf-ocr-storage-local.toml"
        )

        self.config = Configula(
            config_locations=[self.toml_file]
        )

    def test_broker(self):
        section_name = 'redis'
        host = self.config.get(section_name, 'host')
        password = self.config.get(section_name, 'password')
        port = self.config.get(section_name, 'port')
        db = self.config.get(section_name, 'db')
        transport_options = self.config.get(section_name, 'transport_options')
        connection_retry_on_startup = self.config.get(section_name, 'connection_retry_on_startup')
        result = dict(
            url=f'redis://:{password}@{host}:{port}/{db}',
            transport_options=dict(
                max_retries=transport_options['max_retries'],
                interval_start=transport_options['interval_start'],
                interval_step=transport_options['interval_step'],
                interval_max=transport_options['interval_max'],
            ),
            connection_retry_on_startup=connection_retry_on_startup
        )
        print("result=%s" % result)
        assert result is not None

    def test_json(self):
        arrays = ["adsf", "adsfads", ["xzCxz", "xzcxz", 1232], 1, 21312, "12321"]
        str_array = str(json.dumps(arrays))
        print(str_array)
        str_array = ",".join(str(i) for i in arrays)
        print(str_array)
