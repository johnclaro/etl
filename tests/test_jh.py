import unittest
import pandas as pd
import numpy as np

from etl import settings
from etl.covid.johnhopkins.source import JohnHopkins


class TestJH(unittest.TestCase):

    def setUp(self):
        data = {
            'Date': ['2020-01-22', '2020-01-22'],
            'Country/Region': ['US', 'US'],
            'Province/State': [np.NaN, np.NaN],
            'Confirmed': [1, 2],
            'Recovered': [1.0, 2.0],
            'Deaths': [1, 2]
        }
        self.df = pd.DataFrame(data=data)
        settings.DATASET = 'cases'
        self.johnhopkins = JohnHopkins()

    def test_transform(self):
        items = self.johnhopkins.transform(self.df)
        for item in items:
            self.assertTrue('Ireland', item['country'])


if __name__ == '__main__':
    unittest.main()
