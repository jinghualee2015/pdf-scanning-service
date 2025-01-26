import logging
from urllib.parse import quote

from pdf_ocr_service.configula.pdf_ocr_config import DmsServiceConfig, OssConfig, AiConfig, \
    SummaryModelInfo, EmbeddingModelInfo
from pdf_ocr_service.configula import Configula
from celery._state import get_current_task

config = Configula()


class TaskLogFormatter(logging.Formatter):
    def format(self, record):
        task = get_current_task()
        if task and task.request:
            record.__dict__.update(
                task_id='%s ' % task.request.id,
                task_name='%s ' % task.name
            )
        else:
            record.__dict__.setdefault('task_name', '')
            record.__dict__.setdefault('task_id', '')

        return logging.Formatter.format(self, record)


class ConfigUtils(object):
    def __init__(self):
        self.config = config

    def get_main_config(self) -> dict:
        """

        :return: main相关配置
        """
        section_name = 'main'
        return dict(
            tmp_pdf_path=self.config.get(section_name, 'tmp_pdf_path'),
            app_name=self.config.get(section_name, 'app_name'),
            default_language=self.config.get(section_name, 'default_language'),
        )

    def get_storage_config(self) -> OssConfig:
        """

        :return: MinIO配置
        """
        section_name = 'storage'
        host = self.config.get(section_name, 'host')
        port = self.config.get(section_name, 'port')
        access_key = self.config.get(section_name, 'access_key')
        secret_key = self.config.get(section_name, 'secret_key')
        secure = self.config.get(section_name, 'secure')
        bucket_name = self.config.get(section_name, 'bucket_name')
        region = self.config.get(section_name, 'region')

        oss_config = OssConfig(host=host, port=port, access_key=access_key, secret_key=secret_key, secure=secure,
                               bucket_name=bucket_name, region=region)
        return oss_config

    def get_dms_service_config(self) -> DmsServiceConfig:
        """

        :return: DMS-Service配置
        """
        section_name = 'dms-service'
        host = self.config.get(section_name, 'host')
        port = self.config.get(section_name, 'port')
        schema = self.config.get(section_name, 'schema')
        path = self.config.get(section_name, 'path')
        method = self.config.get(section_name, 'method')
        headers = self.config.get(section_name, 'headers')
        dms_service_cfg = DmsServiceConfig(host=host, schema=schema, port=port, path=path, method=method,
                                           headers=headers)
        return dms_service_cfg

    def get_log_config(self) -> dict:
        """

        :return: 日志相关配置
        """
        section_name = "logger"
        worker_cfg: dict = self.config.get(section_name, 'worker_config', dict())
        task_cfg: dict = self.config.get(section_name, 'task_config', dict())
        log_config = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "task_formatter": {
                    "class": "pdf_ocr_service.utils.config_utils.TaskLogFormatter",
                    "format": "[%(asctime)s: %(levelname)s/%(processName)s] %(task_name)s[%(task_id)s]: %(message)s"
                },
                "worker_formatter": {
                    "class": "pdf_ocr_service.utils.config_utils.TaskLogFormatter",
                    "format": "[%(asctime)s: %(levelname)s/%(processName)s] %(message)s"
                },
            },
            "handlers": {
                "task_log_handler": {
                    "level": "INFO",
                    "class": "concurrent_log_handler.ConcurrentRotatingFileHandler",
                    "maxBytes": task_cfg.get('max_bytes'),
                    "backupCount": task_cfg.get('backup_count'),
                    "filename": task_cfg.get('log_file', './logs/tasks.log'),
                    "formatter": "task_formatter",
                    "encoding": "utf-8",
                    "use_gzip": True
                },
                "worker_log_handler": {
                    "level": "INFO",
                    "class": "concurrent_log_handler.ConcurrentRotatingFileHandler",
                    "maxBytes": worker_cfg.get('max_bytes'),
                    "backupCount": worker_cfg.get('backup_count'),
                    "filename": worker_cfg.get('log_file', './logs/worker.log'),
                    "formatter": "worker_formatter",
                    "encoding": "utf-8",
                    "use_gzip": True
                }
            },
            "loggers": {
                "ocr.task": {
                    "handlers": ["task_log_handler", ],
                    "propagate": True,
                    "level": task_cfg.get('log_level'),
                },
                "ocr.worker": {
                    "handlers": ["worker_log_handler", ],
                    "propagate": True,
                    "level": worker_cfg.get('log_level'),
                }
            }
        }
        return log_config

    def get_celery_config(self) -> dict:
        """

        :return: Celery 应用相关配置
        """
        section_name = 'celery'
        worker_concurrency = self.config.get(section_name, 'worker_concurrency')
        worker_prefetch_multiplier = self.config.get(section_name, 'worker_prefetch_multiplier')
        accept_content = self.config.get(section_name, 'accept_content')
        result_serializer = self.config.get(section_name, 'result_serializer')
        task_imports = self.config.get(section_name, 'task_imports')
        worker_log_format = self.config.get(section_name, 'worker_log_format')
        task_log_format = self.config.get(section_name, 'task_log_format')
        return dict(
            worker_concurrency=worker_concurrency,
            worker_prefetch_multiplier=worker_prefetch_multiplier,
            accept_content=accept_content,
            result_serializer=result_serializer,
            task_imports=task_imports,
            worker_log_format=worker_log_format,
            task_log_format=task_log_format
        )

    def get_task_config(self) -> dict:
        """

        :return: Task相关配置
        """
        section_name = 'tasks'
        queues = self.config.get(section_name, 'queues')
        routes = self.config.get(section_name, 'routes')
        acks_on_failure_or_timeout = self.config.get(section_name, 'acks_on_failure_or_timeout')
        default_routing_key = self.config.get(section_name, 'default_routing_key')
        default_exchange = self.config.get(section_name, 'default_exchange')
        default_exchange_type = self.config.get(section_name, 'default_exchange_type')
        return dict(
            queues=queues,
            routes=routes,
            acks_on_failure_or_timeout=acks_on_failure_or_timeout,
            default_routing_key=default_routing_key,
            default_exchange=default_exchange,
            default_exchange_type=default_exchange_type
        )

    def get_broker_config(self) -> dict:
        """

        :return: Broker Redis 配置信息
        """
        STAND_ALONE = 'standalone'
        SENTINEL = 'sentinel'
        CLUSTER = 'cluster'
        section_name = 'redis'
        redis_type = self.config.get(section_name, 'type', 'standalone')
        hosts = self.config.get(section_name, 'hosts')
        password = self.config.get(section_name, 'password')
        # port = self.config.get(section_name, 'port')
        db = self.config.get(section_name, 'db')
        transport_options = self.config.get(section_name, 'transport_options')
        connection_retry_on_startup = self.config.get(section_name, 'connection_retry_on_startup')
        if redis_type == STAND_ALONE:
            password = quote(password)
            redis_url = f'redis://:{password}@{hosts[0].get("host")}:{hosts[0].get("port")}/{db}'
        elif redis_type == SENTINEL:
            redis_url = ''
            for host in hosts:
                redis_url += f'sentinel://:{password}@{host.get("host")}:{host.get("port")}/{db};'
            redis_url = redis_url[:-1]
        else:
            raise Exception("Not support Redis type")

        ret = dict(
            url=redis_url,
            transport_options=dict(
                max_retries=transport_options['max_retries'],
                interval_start=transport_options['interval_start'],
                interval_step=transport_options['interval_step'],
                interval_max=transport_options['interval_max'],
            ),
            connection_retry_on_startup=connection_retry_on_startup
        )
        if redis_type == SENTINEL:
            sentinel_kwargs = {
                'password': password,
            }
            ret['transport_options']['master_name'] = transport_options['master_name']
            ret['transport_options']['sentinel_kwargs'] = sentinel_kwargs
        return ret

    def get_backend_config(self) -> dict:
        """

        :return: Backend Database 配置
        """
        section_name = 'database'
        db_type = self.config.get(section_name, 'db_type')
        host = self.config.get(section_name, 'host')
        port = self.config.get(section_name, 'port')
        user = self.config.get(section_name, 'user')
        password = self.config.get(section_name, 'password')
        password = quote(password)
        db = self.config.get(section_name, 'db')
        engine_options = self.config.get(section_name, 'engine_options')
        table_schemas = self.config.get(section_name, 'table_schemas')
        table_names = self.config.get(section_name, 'table_names')

        return dict(
            url=f"db+{db_type}://{user}:{password}@{host}:{port}/{db}",
            normal_url=f"{db_type}://{user}:{password}@{host}:{port}/{db}",
            engine_options=dict(
                echo=engine_options['echo'],
            ),
            table_schemas=dict(
                task=table_schemas['task'],
                group=table_schemas['group'],
            ),
            table_names=dict(
                task=table_names['task'],
                group=table_names['group'],
            )

        )

    def get_ai_config(self) -> AiConfig:
        """
        Return Ai related configuration
        """
        section_name = 'ai'
        access_key = self.config.get(section_name, 'access_key', '')
        secret_key = self.config.get(section_name, 'secret_key', '')
        service_name = self.config.get(section_name, 'service_name', '')
        accept = self.config.get(section_name, 'accept', '')
        content_type = self.config.get(section_name, 'content_type', '')
        region_name = self.config.get(section_name, 'region_name', '')
        embedding: dict = self.config.get(section_name, 'embedding', dict())
        summary: dict = self.config.get(section_name, 'summary', dict())
        embedding_model = EmbeddingModelInfo(model_id=embedding.get('model_id'),
                                             input_type=embedding.get('input_type'))
        summary_model = SummaryModelInfo(model_id=summary.get('model_id'),
                                         max_tokens_to_sample=summary.get('max_tokens_to_sample'),
                                         temperature=summary.get('temperature'),
                                         stop_sequences=summary.get('stop_sequences'))
        return AiConfig(
            access_key=access_key,
            secret_key=secret_key,
            service_name=service_name,
            accept=accept,
            content_type=content_type,
            region_name=region_name,
            embedding=embedding_model,
            summary=summary_model
        )
