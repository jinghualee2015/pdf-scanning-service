import os
import unittest
import pandas as pd


class PandasSeriesTest(unittest.TestCase):

    def test_01(self):
        a = [1, 2, 3, 4, 5, 6]
        myvar = pd.Series(a)
        print(myvar)

    def test_02(self):
        a = ["Google", "Runoob", "Wiki"]
        myvar = pd.Series(a, index=["x", "y", "z"])
        print(myvar)
        print(myvar["y"])

    def test_3(self):
        sites = {1: "Google",
                 2: "Runoob",
                 3: "Wiki"}
        myvar = pd.Series(sites)
        print(myvar)

    def test_4(self):
        sites = {1: "Google",
                 2: "Runoob",
                 3: "Wiki"}
        myvar = pd.Series(sites, index=[1, 2, ])
        print(myvar)

    def test_05(self):
        sites = {1: "Google",
                 2: "Runoob",
                 3: "Wiki"}
        myvar = pd.Series(sites, index=[1, 2, ], name="Dafadsfadsf")

        print(myvar)


class PandasDataFrameTest(unittest.TestCase):
    def test_01(self):
        data = [
            ['Google', 10],
            ['Runoob', 12],
            ['Wiki', 13]
        ]
        df = pd.DataFrame(data, columns=['Site', 'Age'])
        df['Site'] = df['Site'].astype(str)
        df['Age'] = df['Age'].astype(float)

        print(df)

    def test_02(self):
        data = {
            'Site': ['Google', 'Runoob', 'Wiki'],
            'Age': [10, 12, 13],
        }
        df = pd.DataFrame(data=data)
        print(df)

    def test_03(self):
        data = [{'a': 1, 'b': 2}, {'a': 5, 'b': 10, 'c': 20}]
        df = pd.DataFrame(data)

        print(df)

    def test_04(self):
        data = {
            "calories": [420, 280, 390],
            "duration": [50, 40, 45],
        }
        df = pd.DataFrame(data)
        print(df.loc[0])
        print(df.loc[1])

    def test_05(self):
        data = {
            "calories": [420, 280, 390],
            "duration": [50, 40, 45],
        }
        df = pd.DataFrame(data)
        print(df.loc[[0, 1]])

    def test_06(self):
        data = {
            "calories": [420, 280, 390],
            "duration": [50, 40, 45],
        }
        df = pd.DataFrame(data, index=["day1", "day2", "day3"])
        print(df)
        print(df.loc["day2"])


class PandasCsvTest(unittest.TestCase):
    def setUp(self):
        self.csv_file = os.path.join(os.path.dirname(__file__), "../examples", "nba.csv")
        self.file_base_path = os.path.join(os.path.dirname(__file__), "../examples")

    def test_01(self):
        df = pd.read_csv(self.csv_file)
        print(df.to_string())

    def test_02(self):
        df = pd.read_csv(self.csv_file)
        print(df)

    def test_03(self):
        nme = ["Google", "Runoob", "Taobao", "Wiki"]
        st = ["www.google.com", "www.runoob.com", "www.taobao.com", "www.wikipedia.org"]
        ag = [90, 40, 80, 98]
        dict = {'name': nme, 'site': st, 'age': ag}

        df = pd.DataFrame(dict)
        df.to_csv(os.path.join(self.file_base_path, "site.csv"))

    def test_04(self):
        df = pd.read_csv(self.csv_file)
        print(df.head(10))

    def test_05(self):
        df = pd.read_csv(self.csv_file)
        print(df.tail(10))

    def test_06(self):
        df = pd.read_csv(self.csv_file)
        print(df.info(10))
