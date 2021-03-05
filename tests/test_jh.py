import unittest
import pandas as pd
import numpy as np

import etl


class TestJH(unittest.TestCase):

    def setUp(self):
        data = {
            'Date': ['2020-01-22', '2020-01-22'],
            'Country/Region': ['Ireland', 'US'],
            'Province/State': [np.NaN, np.NaN],
            'Confirmed': [1, 2],
            'Recovered': [1.0, 2.0],
            'Deaths': [1, 2]
        }
        self.df = pd.DataFrame(data=data)

    def test_transform(self):
        df = etl.sources.jh.transform(self.df)
        self.assertTrue('Ireland' not in df.values)


if __name__ == '__main__':
    unittest.main()
