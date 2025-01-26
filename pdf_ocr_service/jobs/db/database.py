from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pdf_ocr_service.factory.app_factory import get_config_utils
from pdf_ocr_service.celery import task_logger

logger = task_logger

SQLALCHEMY_DATABASE_URL = get_config_utils().get_backend_config().get('normal_url')
engine = create_engine(SQLALCHEMY_DATABASE_URL,
                       pool_size=20,
                       pool_pre_ping=True,
                       pool_use_lifo=True,
                       pool_recycle=600)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


@contextmanager
def get_session():
    session = Session()
    try:
        yield session
        logger.debug("commit session....")
        session.commit()
    except Exception as ex:
        logger.warning(f"get session occur error:{str(ex)}")
        session.rollback()
    finally:
        logger.debug("close session....")
        session.close()
