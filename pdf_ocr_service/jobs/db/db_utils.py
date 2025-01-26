from pdf_ocr_service.jobs.db import DmsDocuments, DmsDocumentVersions, DmsDocumentsProcessTasks, DmsDocumentEmbedding
from pdf_ocr_service.jobs.domains import EmbeddingToken
from pdf_ocr_service.jobs.domains.document_process_result import DocumentProcessResult
from pdf_ocr_service.jobs.db.database import get_session
from pdf_ocr_service.celery import task_logger
from sqlalchemy import and_

logger = task_logger


def update_process_content(process_result: DocumentProcessResult) -> bool:
    """
    update process result to dbms
    just update document and version content data not modify process_status
    :param process_result processor process document result
    :return: update result, True means success, False mean failed
    """
    with get_session() as session:
        logger.debug(
            f"update_process_content  result status {process_result.get_status()} error_msg:{process_result.get_error_msg()}")
        document: DmsDocuments = __get_document(session=session,
                                                document_id=process_result.get_document_id(),
                                                )
        if document is None:
            logger.warning(f"can not find document with id:{process_result.get_document_id()}")
            return False
        version: DmsDocumentVersions = __get_version(session=session,
                                                     document_id=process_result.get_document_id(),
                                                     version=process_result.get_version(),
                                                     )
        if version is None:
            logger.warning(
                f"can not find version with document_id:{process_result.get_document_id()} and version:{process_result.get_version()}")
            return False
        task: DmsDocumentsProcessTasks = __get_task(session=session,
                                                    document_id=process_result.get_document_id(),
                                                    version=process_result.get_version(),
                                                    task_id=process_result.get_task_id()
                                                    )
        if task is None:
            logger.warning(
                f"can not find task with document_id:{process_result.get_document_id()} "
                f" and version:{process_result.get_version()} "
                f"and task_id:{process_result.get_task_id()}"
            )
            return False

        document.content = process_result.get_content()
        version.content = process_result.get_content()
        version.url = process_result.get_file_path()
        version.abstracts = process_result.get_summary() if process_result.get_summary() is not None else ''
        version.is_embedding = True if len(process_result.get_tokens()) > 0 else False
        task.status = process_result.get_status()
        task.is_complete = True
        task.process_file_url = process_result.get_file_path()
        task.side_car_file_url = process_result.get_side_car_path() if process_result.get_side_car_path() is not None else ''

        session.add(document)
        session.add(version)
        session.add(task)
        _add_embeddings(session, document, version, process_result.get_tokens())
    return True


def update_ocr_result(process_result: DocumentProcessResult) -> bool:
    """
    update ocr process result to dbms
    just update document and version content data and  process_status
    :param process_result processor process document result
    :return: update result, True means success, False mean failed
    """
    with get_session() as session:
        logger.debug(
            f"update_ocr_result result status {process_result.get_status()} error_msg:{process_result.get_error_msg()}")

        document: DmsDocuments = __get_document(session=session,
                                                document_id=process_result.get_document_id(),
                                                )
        if document is None:
            logger.warning(f"can not find document with id:{process_result.get_document_id()}")
            return False
        version: DmsDocumentVersions = __get_version(session=session,
                                                     document_id=process_result.get_document_id(),
                                                     version=process_result.get_version(),
                                                     )
        if version is None:
            logger.warning(
                f"can not find version with document_id:{process_result.get_document_id()} and version:{process_result.get_version()}")
            return False
        task: DmsDocumentsProcessTasks = __get_task(session=session,
                                                    document_id=process_result.get_document_id(),
                                                    version=process_result.get_version(),
                                                    task_id=process_result.get_task_id()
                                                    )
        if task is None:
            logger.warning(
                f"can not find task with document_id:{process_result.get_document_id()} "
                f" and version:{process_result.get_version()} "
                f"and task_id:{process_result.get_task_id()}"
            )
            return False

        document.content = process_result.get_content()
        document.process_pending = False
        document.process_status = process_result.get_status()
        document.process_exception = process_result.get_error_msg() if process_result.get_error_msg() is not None else 'OK'
        version.content = process_result.get_content()
        version.process_status = process_result.get_status()
        version.url = process_result.get_file_path()
        version.abstracts = process_result.get_summary() if process_result.get_summary() is not None else ''
        version.is_embedding = True if len(process_result.get_tokens()) > 0 else False
        task.status = process_result.get_status()
        task.is_complete = True
        task.process_file_url = process_result.get_file_path()
        task.side_car_file_url = process_result.get_side_car_path() if process_result.get_side_car_path() is not None else ''

        session.add(document)
        session.add(version)
        session.add(task)
        _add_embeddings(session, document, version, process_result.get_tokens())
    return True


def _add_embeddings(session, document: DmsDocuments,
                    version: DmsDocumentVersions,
                    embeddings: list[EmbeddingToken]):
    """
    add document embeddings
    :param session: db session instance
    :param document: DmsDocument instance
    :param version DmsDocumentVersions instance
    :param embeddings: EmbeddingToken list
    """
    db_embeddings = list[DmsDocumentEmbedding]()
    for embedding in embeddings:
        db_embeddings.append(
            DmsDocumentEmbedding(
                doc_id=document.id,
                version=version.version,
                title=document.name,
                tokens=embedding.get_token(),
                page_number=embedding.get_pages(),
                block_number=embedding.get_block_num(),
                embedding=embedding.get_embeddings(),
                positions=embedding.get_positions(),
            )
        )
    delete_rows = session.query(DmsDocumentEmbedding).filter(
        and_(DmsDocumentEmbedding.doc_id == document.id,
             DmsDocumentEmbedding.version == version.version)).delete()
    logger.info(f"document[{document.id}] version:[{version.version}] delete old embeddings [{delete_rows}]")
    if len(db_embeddings) > 0:
        session.add_all(db_embeddings)


def __get_document(session, document_id: int):
    document: DmsDocuments = session.query(DmsDocuments).filter(
        DmsDocuments.id == document_id).first()
    return document


def __get_version(session, document_id: int, version: int):
    version: DmsDocumentVersions = session.query(DmsDocumentVersions).filter(
        DmsDocumentVersions.doc_id == document_id,
        DmsDocumentVersions.version == version
    ).first()

    return version


def __get_task(session, document_id: int, version: int, task_id: str):
    task: DmsDocumentsProcessTasks = session.query(DmsDocumentsProcessTasks).filter(
        DmsDocumentsProcessTasks.task_id == task_id,
        DmsDocumentsProcessTasks.doc_id == document_id,
        DmsDocumentsProcessTasks.version == version
    ).first()

    return task
