import unittest
import pandas as pd
import numpy as np

from covid import transform


class TestTransform(unittest.TestCase):

    def setUp(self):
        index = ['2020-01-22']
        data = {
            'Country/Region': ['Ireland'],
            'Province/State': [np.NaN],
            'Confirmed': [0],
            'Recovered': [0.0],
            'Deaths': [0]
        }
        self.df = pd.DataFrame(index=index, data=data)

    def test_columns_forward_slash(self):
        df = transform(self.df)
        columns = [
            'country_region',
            'province_state',
            'confirmed',
            'recovered',
            'deaths'
        ]
        for index, column in enumerate(df.columns):
            self.assertEqual(column, columns[index])


if __name__ == '__main__':
    unittest.main()
