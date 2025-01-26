import os.path
import unittest
from urllib.parse import quote

from pdf_ocr_service.configula import Configula


class TestConfigula(unittest.TestCase):
    def setUp(self):
        self.toml_file = os.path.join(
            os.path.dirname(__file__), "../examples", "pdf-ocr-service.toml"
        )

        self.configula = Configula(
            config_locations=[self.toml_file]
        )

    def test_database(self):
        section_name = 'database'
        database_host = self.configula.get(section_name, 'host', '12')
        database_port = self.configula.get(section_name, 'port', -1)
        database_user = self.configula.get(section_name, 'user', 'admin')
        assert database_host == 'localhost'
        assert database_port == 5432
        assert database_user == 'john'

    def test_ocr(self):
        section_name = 'ocr'
        language = self.configula.get(section_name, 'default_language', 'deu')
        assert language == 'eng'

    def test_redis(self):
        STAND_ALONE = 'standalone'
        SENTINEL = 'sentinel'
        CLUSTER = 'cluster'
        section_name = 'redis'
        redis_type = self.configula.get(section_name, 'type', 'standalone')
        hosts = self.configula.get(section_name, 'hosts')
        password = self.configula.get(section_name, 'password')
        password = quote(password)
        db = self.configula.get(section_name, 'db')
        transport_options = self.configula.get(section_name, 'transport_options')
        connection_retry_on_startup = self.configula.get(section_name, 'connection_retry_on_startup')
        if redis_type == STAND_ALONE:
            redis_url = f'redis://:{password}@{hosts[0].get("host")}:{hosts[0].get("port")}/{db}'
        elif redis_type == SENTINEL:
            redis_url = ''
            for host in hosts:
                redis_url += f'sentinel://{password}@{host.get("host")}:{host.get("port")}/{db};'
            redis_url = redis_url[:-1]
        else:
            raise Exception("Not support Redis type")

        return dict(
            url=redis_url,
            transport_options=dict(
                max_retries=transport_options['max_retries'],
                interval_start=transport_options['interval_start'],
                interval_step=transport_options['interval_step'],
                interval_max=transport_options['interval_max'],
                master_name=transport_options['master_name'],
            ),
            connection_retry_on_startup=connection_retry_on_startup
        )

    def test_map(self):
        section_name = 'jobs'
        queues = self.configula.get(section_name, "queues")
        # print(type(queues))
        print(queues)

    def test_log_config(self):
        log_cfg = self.configula.get('logger_base', 'value', dict())
        logger_formatters = self.configula.get('logger_formatters', 'value', dict())
        logger_handlers = self.configula.get('logger_handlers', 'value', dict())
        logger_loggers = self.configula.get('logger_loggers', 'value', dict())
        WORKER_LOG_CONFIG = log_cfg
        WORKER_LOG_CONFIG['formatters'] = logger_formatters
        WORKER_LOG_CONFIG['handlers'] = logger_handlers
        WORKER_LOG_CONFIG['loggers'] = logger_loggers
        print("WORKER_LOG_CONFIG=%s" % WORKER_LOG_CONFIG)
