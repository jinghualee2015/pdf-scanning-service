from celery import Celery

from pdf_ocr_service.utils.config_utils import ConfigUtils
from pdf_ocr_service.configula.pdf_ocr_config import PdfOcrConfig
import logging.config as log_config

config_utils = ConfigUtils()
LOG_CFG = config_utils.get_log_config()
log_config.dictConfig(config=LOG_CFG)
service_config = PdfOcrConfig(main_config=config_utils.get_main_config(),
                              oss_cfg=config_utils.get_storage_config(),
                              dms_cfg=config_utils.get_dms_service_config(),
                              ai_cfg=config_utils.get_ai_config(),
                              )


def get_config_utils():
    return config_utils


def get_celery() -> Celery:
    app_name = service_config.app_name
    broker_info = config_utils.get_broker_config()
    backend_info = config_utils.get_backend_config()
    celery_info = config_utils.get_celery_config()
    task_info = config_utils.get_task_config()
    app = Celery(
        main=app_name,
        broker=broker_info.get('url'),
        backend=backend_info.get('url'),
    )

    app.conf.broker_transport_options = broker_info.get('transport_options')
    app.conf.broker_connection_retry_on_startup = broker_info.get('connection_retry_on_startup')
    app.conf.database_engine_options = backend_info.get('engine_options')
    app.conf.database_table_names = backend_info.get('table_names')

    app.conf.worker_concurrency = celery_info.get('worker_concurrency')
    app.conf.worker_prefetch_multiplier = celery_info.get('worker_prefetch_multiplier')
    app.conf.accept_content = celery_info.get('accept_content')
    app.conf.result_serializer = celery_info.get('result_serializer')
    app.conf.imports = celery_info.get('task_imports')
    # app.conf.worker_log_format = celery_info.get('worker_log_format')
    # app.conf.worker_task_log_format = celery_info.get('worker_task_log_format')
    app.conf.timezone = celery_info.get('timezone')
    app.conf.enable_utc = celery_info.get('enable_utc')

    app.conf.task_queues = task_info.get('queues')
    app.conf.task_routes = task_info.get('routes')
    app.conf.task_default_exchange = task_info.get('default_exchange')
    app.conf.task_default_exchange_type = task_info.get('default_exchange_type')
    app.conf.task_default_routing_key = task_info.get('default_routing_key')
    app.conf.task_acks_on_failure_or_timeout = task_info.get('acks_on_failure_or_timeout')

    return app
