from .token_postion import TokenPosition
from .document_embedding_token import EmbeddingToken
from langchain.schema import Document


class DocumentProcessResult(object):
    """
    Extract PDF Result
    """

    def __init__(self,
                 document_id: int = None,
                 version: int = None,
                 task_id: str = None,
                 ):
        self._document_id = document_id
        self._version = version
        self._task_id = task_id
        self._status = True
        self._error_msg = ''
        self._file_path = None
        self._side_car_path = None
        self._content = None
        self._tokens: list[EmbeddingToken] = []
        self._summary = ''
        self._page_contents: list[Document] = []
        self._page_positions: dict[str, list[TokenPosition]] = {}

    def get_summary(self):
        return self._summary

    def set_summary(self, summary):
        self._summary = summary

    def get_status(self):
        return self._status

    def set_status(self, status: bool = None):
        self._status = status

    def get_error_msg(self):
        return self._error_msg

    def set_error_msg(self, error_msg: str = None):
        self._error_msg = error_msg

    def get_document_id(self):
        return self._document_id

    def get_version(self):
        return self._version

    def get_task_id(self):
        return self._task_id

    def get_file_path(self):
        return self._file_path

    def set_file_path(self, file_path: str = None):
        self._file_path = file_path

    def get_content(self):
        return self._content

    def set_content(self, content: str = None):
        self._content = content

    def get_side_car_path(self):
        return self._side_car_path

    def set_side_car_path(self, side_car_path: str = None):
        self._side_car_path = side_car_path

    def get_tokens(self):
        if self._tokens is None:
            self._tokens = []
        return self._tokens

    def add_token(self, token: EmbeddingToken):
        self._tokens.append(token)

    def remove_token(self, token: EmbeddingToken):
        self._tokens.remove(token)

    def add_page_content(self, page_content, page_number):
        self._page_contents.append(Document(
            page_content=page_content,
            metadata={
                "source": self._task_id,
                "page": page_number
            }
        ))

    def add_all_page_content(self, contents: list[dict]):
        for content in contents:
            self._page_contents.append(
                Document(
                    page_content=content.get("content"),
                    metadata={
                        "source": self._task_id,
                        "page": content.get("page")
                    }
                )
            )

    def get_page_contents(self) -> list:
        return self._page_contents

    def add_page_positions(self, page_number: int = None,
                           block_number: int = None,
                           positions: list[TokenPosition] = None):
        if not page_number \
                and not block_number \
                and not positions \
                and len(positions) > 0:
            key = DocumentProcessResult.get_page_positions_key(page_number=page_number,
                                                               block_number=block_number)
            self._page_tokens.update({key: positions})

    def get_page_positions(self, page_number: int = None,
                           block_number: int = None) -> list[TokenPosition]:
        if not page_number \
                and not block_number:
            key = DocumentProcessResult.get_page_positions_key(page_number=page_number,
                                                               block_number=block_number)
            return self._page_tokens.get(key) or []
        return []

    @classmethod
    def get_page_positions_key(cls, page_number: int = None,
                               block_number: int = None):
        return f'{page_number}-{block_number}'

    def __del__(self):
        self._page_positions.clear()
        self._page_positions = None
        self._page_contents.clear()
        self._page_contents = None
        self._tokens.clear()
        self._tokens = None
