import unittest

import kombu


class SentinelTest(unittest.TestCase):
    def setUp(self):
        password = "WjEAN5Ud"
        self.url = f'sentinel://:{password}@redis-sentinel1:26379/2;sentinel://:{password}@redis-sentinel2:26380/2;sentinel://:{password}@redis-sentinel3:26381/2'
        self.transport_options = {
            'master_name': 'nyquistdata-redis',
            'sentinel_kwargs': {
                'password': password
            }
        }

    def test_connect(self):
        conn = kombu.Connection(self.url, transport_options=self.transport_options)
        conn.connect()
