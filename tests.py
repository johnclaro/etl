import unittest
import pandas as pd
import numpy as np

from covid import transform


class TestTransform(unittest.TestCase):

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

    def test_country_us_only(self):
        df = transform(self.df)
        self.assertTrue('Ireland' not in df.values)

    def test_columns_forward_slash(self):
        df = transform(self.df)
        columns = [
            'date',
            'country',
            'state',
            'cases',
            'recovered',
            'deaths'
        ]
        for index, column in enumerate(df.columns):
            self.assertEqual(column, columns[index])


if __name__ == '__main__':
    unittest.main()
