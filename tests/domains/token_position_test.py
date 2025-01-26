import unittest
import random

from pdf_ocr_service.jobs.domains import TokenPosition


class TokenPositionTest(unittest.TestCase):

    def test_01(self):
        p = TokenPosition(
            left=random.uniform(1.0, 20.0),
            right=random.uniform(1.0, 20.0),
            top=random.uniform(1.0, 20.0),
            bottom=random.uniform(1.0, 20.0),
        )
        print(f'position is {p}')

    def test_02(self):
        positions: list[TokenPosition] = []
        l_p = TokenPosition(
            left=0.00,
            top=0.00,
            right=2048,
            bottom=1000,
        )
        positions.append(l_p)
        s_p = TokenPosition(
            left=10.00,
            top=10.00,
            right=1024,
            bottom=600,
        )
        if s_p not in positions:
            positions.append(s_p)
        print(positions)
