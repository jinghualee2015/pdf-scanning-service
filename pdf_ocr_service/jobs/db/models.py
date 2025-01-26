from sqlalchemy import Integer, String, Boolean, BigInteger, SmallInteger
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql.schema import Column
from pgvector.sqlalchemy import Vector
from pdf_ocr_service.jobs.db.database import Base


class DmsDocuments(Base):
    """
    table dms_documents entity
    """
    __tablename__ = 'dms_documents'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    content = Column(String, nullable=True)
    process_pending = Column(Boolean, nullable=True)
    process_status = Column(Boolean, nullable=True)
    process_exception = Column(String, nullable=True)


class DmsDocumentVersions(Base):
    """
    table dms_document_versions entity
    """
    __tablename__ = 'dms_document_versions'
    id = Column(Integer, primary_key=True)
    doc_id = Column(Integer, nullable=False)
    version = Column(SmallInteger, nullable=False)
    content = Column(String, nullable=True)
    url = Column(String, nullable=True)
    process_status = Column(Boolean, nullable=True)
    abstracts = Column(String, nullable=True)
    is_embedding = Column(Boolean, nullable=False, default=False)


class DmsDocumentsProcessTasks(Base):
    """
    table dms_documents_process_tasks entity
    """
    __tablename__ = 'dms_documents_process_tasks'
    id = Column(BigInteger, primary_key=True)
    task_id = Column(String, nullable=False)
    doc_id = Column(Integer, nullable=False)
    version = Column(SmallInteger, nullable=False)
    status = Column(Boolean, nullable=True)
    is_complete = Column(Boolean, nullable=True)
    process_file_url = Column(String, nullable=True)
    side_car_file_url = Column(String, nullable=True)


class DmsDocumentEmbedding(Base):
    """
    table dms_document_embedding entity
    """
    __tablename__ = 'dms_document_embedding'
    id = Column(Integer, primary_key=True)
    doc_id = Column(Integer, nullable=False)
    version = Column(SmallInteger, nullable=False)
    title = Column(String, nullable=True)
    tokens = Column(String, nullable=False)
    page_number = Column(Integer, nullable=True)
    block_number = Column(Integer, nullable=True)
    embedding = mapped_column(Vector(1024), nullable=True)
    positions = Column(String, nullable=True)
