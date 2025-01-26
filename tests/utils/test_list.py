import unittest


class ListTest(unittest.TestCase):
    def test_01(self):
        arrs: list(int) = list()
        arrs.append([1, 3, 3, 45, 6])
        print(arrs)
        arrs.append([1, 3, 6])
        print(arrs)

    def test_01(self):
        arrs: list(int) = list()
        arrs.extend([1, 3, 3, 45, 6])
        print(arrs)
        arrs.extend([1, 3, 6])
        print(arrs)
