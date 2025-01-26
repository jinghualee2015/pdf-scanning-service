import unittest
import random


class Rect:
    x0: float = 0.00
    x1: float = 0.00
    y0: float = 0.00
    y1: float = 0.00

    def __init__(self, x0: float = None, x1: float = None, y0: float = None, y1: float = None):
        self.x0 = x0
        self.x1 = x1
        self.y0 = y0
        self.y1 = y1

    def __str__(self):
        return f'x0={self.x0}, x1={self.x1}, y0={self.y0}, y1={self.y1}'

    def __repr__(self):
        return f'<x0={self.x0} , y0={self.y0} , x1={self.x1}, y1={self.y1}>'


class SortedTest(unittest.TestCase):

    def test_01(self):
        positions = []
        for i in range(20):
            positions.append(
                Rect(x0=random.uniform(1.0, 20.0),
                     x1=random.uniform(1.0, 20.0),
                     y0=random.uniform(1.0, 20.0),
                     y1=random.uniform(1.0, 20.0)
                     )
            )

        print(positions)
        positions = sorted(positions, key=lambda r: (r.x0, r.y0, r.x1, r.y1))
        for p in positions:
            print(p)
