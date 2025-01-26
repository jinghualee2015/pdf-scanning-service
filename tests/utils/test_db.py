import unittest
from pdf_ocr_service.jobs.db.models import DmsDocuments, DmsDocumentEmbedding
from pdf_ocr_service.jobs.db.database import get_session


class DbTest(unittest.TestCase):

    def test_search_document(self):
        with get_session() as session:
            document: DmsDocuments = session.query(DmsDocuments).filter(DmsDocuments.id == 1986).first()
            print(
                f"document id={document.id} pending_ocr={document.pending_ocr} status={document.ocr_status} exception={document.ocr_exception}")
            document.ocr_status = False
            document.ocr_exception = 'parse document occur error'
            document.content = 'python unit test update content....'
            session.add(document)

    def test_vector(self):
        doc = list()
        for index in range(0, 10):
            embedings = [i for i in range(1, 1025)]
            embedding = DmsDocumentEmbedding(
                doc_id=1986,
                version=1,
                title='test document',
                tokens='Hello world just token test',
                page_number=12,
                embedding=embedings
            )
            doc.append(embedding)
        with get_session() as session:
            session.add_all(doc)

    def test_delete_batch(self):
        with get_session() as conn:
            result = conn.query(DmsDocumentEmbedding).filter(DmsDocumentEmbedding.doc_id == 1986).delete()
            print(f"result={result}")
