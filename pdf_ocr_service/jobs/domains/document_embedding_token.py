import json

from .token_postion import TokenPosition


class EmbeddingToken(object):
    """
    Used for store the document embedding information
    """

    def __init__(self,
                 token: str = '',
                 page: int = None,
                 embeddings: list = [],
                 block_num: int = 0,
                 positions: list[TokenPosition] = []
                 ):
        self._token = token
        self._page = page
        self._embeddings = embeddings
        self._block_num = block_num
        self._positions: list[TokenPosition] = positions

    def set_token(self, token: str = None):
        self._token = token

    def get_token(self):
        return self._token

    def set_page(self, page: int = None):
        self._page = page

    def get_pages(self):
        return self._page

    def set_embeddings(self, embeddings: list = []):
        self._embeddings = embeddings

    def get_embeddings(self):
        return self._embeddings

    def get_block_num(self):
        return self._block_num

    def add_position(self, position: TokenPosition = None):
        if position is None:
            return
        self._positions.append(position)

    def get_positions(self) -> str:
        if len(self._positions) <= 0:
            return '[]'
        return json.dumps(self._positions, default=lambda obj: obj.__json__())
