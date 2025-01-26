import math


class TokenPosition(object):
    """
    Token statement occur in document position information bean
    """

    def __init__(self,
                 left: float = 0.00,
                 right: float = 0.00,
                 top: float = 0.00,
                 bottom: float = 0.00,
                 ):
        self._left = TokenPosition.round_data(left)
        self._bottom = TokenPosition.round_data(bottom)
        self._right = TokenPosition.round_data(right)
        self._top = TokenPosition.round_data(top)

    @property
    def left(self):
        return self._left

    @property
    def right(self):
        return self._right

    @property
    def top(self):
        return self._top

    @property
    def bottom(self):
        return self._bottom

    def __json__(self):
        return {
            "left": self._left,
            "right": self._right,
            "top": self._top,
            "bottom": self._bottom
        }

    def __str__(self):
        return f'("top": {self._top}, "left": {self._left}, "bottom": {self._bottom},"right": {self._right})'

    def __eq__(self, other):
        if other is None:
            return False
        if not isinstance(other, TokenPosition):
            return False
        other_p: TokenPosition = other
        if (TokenPosition.is_equals(other_p.top, self._top) and
                TokenPosition.is_equals(other_p.bottom, self._bottom) and
                TokenPosition.is_equals(other_p.left, self._left) and
                TokenPosition.is_equals(other_p.right, self._right)):
            return True
        # if self._top <= other_p.top \
        #         and self._left <= other_p.left \
        #         and self._bottom >= other_p.bottom \
        #         and self._right >= other_p.bottom:
        #     return True
        return False

    def __gt__(self, other):
        if not isinstance(other, TokenPosition):
            return False
        if self._top > other.top \
                and self._left > other.left:
            return True
        return False

    def is_valid(self):
        if (self._left is not None and
                self._right is not None and
                self._top is not None
                and self._bottom is not None):
            return True
        return False

    @classmethod
    def round_data(cls, data: float):
        if data is None:
            return 0.00
        data = round(data, 2)
        return data

    @classmethod
    def is_equals(cls, data1: float, data2: float):
        if data1 is None or data2 is None:
            return False
        if math.fabs(math.fabs(data2) - math.fabs(data1)) <= 0.01:
            return True
        return False
