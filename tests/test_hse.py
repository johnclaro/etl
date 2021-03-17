import unittest

from etl.hse.datasets import HSE


class TestJH(unittest.TestCase):

    def setUp(self):
        self.swabs = HSE('swabs')

    def test_transform_only_one_record(self):
        response = {
            'features': [
                {
                    'attributes': {
                        'Date_HPSC': 1615892400000,
                        'Hospitals': 1277591,
                        'TotalLabs': 3757468,
                        'NonHospitals': 2479877,
                        'Positive': 234622,
                        'PRate': 6.2,
                        'Test24': 11392,
                        'Test7': 99371,
                        'Pos7': 3733,
                        'PosR7': 3.8,
                        'FID': 364
                    }
                }
            ]
        }
        items = self.swabs.transform(response)
        expected_items = [
            {
                'date_hpsc': '2021-03-16',
                'hospitals': 1277591,
                'totallabs': 3757468,
                'nonhospitals': 2479877,
                'positive': 234622,
                'prate': 6.2,
                'test24': 11392,
                'test7': 99371,
                'pos7': 3733,
                'posr7': 3.8,
                'fid': 364,
                'pos1': 234622,
                'posr1': 6.2
            }
        ]
        for index, expected_item in enumerate(expected_items):
            for key, value in expected_item.items():
                self.assertEqual(items[index][key], value)

    def test_transform_multiple_records(self):
        response = {
            'features': [
                {
                    'attributes': {
                        'Date_HPSC': 1615806000000,
                        'Hospitals': 1271124,
                        'TotalLabs': 3746076,
                        'NonHospitals': 2474952,
                        'Positive': 234243,
                        'PRate': 6.3,
                        'Test24': 10586,
                        'Test7': 101564,
                        'Pos7': 3808,
                        'PosR7': 3.7,
                        'FID': 363
                    }
                },
                {
                    'attributes': {
                        'Date_HPSC': 1615892400000,
                        'Hospitals': 1277591,
                        'TotalLabs': 3757468,
                        'NonHospitals': 2479877,
                        'Positive': 234622,
                        'PRate': 6.2,
                        'Test24': 11392,
                        'Test7': 99371,
                        'Pos7': 3733,
                        'PosR7': 3.8,
                        'FID': 364
                    }
                }
            ]
        }
        items = self.swabs.transform(response)
        expected_items = [
            {
                'date_hpsc': '2021-03-15',
                'hospitals': 1271124,
                'totallabs': 3746076,
                'nonhospitals': 2474952,
                'positive': 234243,
                'prate': 6.3,
                'test24': 10586,
                'test7': 101564,
                'pos7': 3808,
                'posr7': 3.7,
                'fid': 363,
                'pos1': 234243,
                'posr1': 6.3,
            },
            {
                'date_hpsc': '2021-03-16',
                'hospitals': 1277591,
                'totallabs': 3757468,
                'nonhospitals': 2479877,
                'positive': 234622,
                'prate': 6.2,
                'test24': 11392,
                'test7': 99371,
                'pos7': 3733,
                'posr7': 3.8,
                'fid': 364,
                'pos1': 379,  # 234622 - 234243
                'posr1': 3.33,  # (379 / (3757468 - 3746076)) * 100 = 3.326
            }
        ]
        for index, expected_item in enumerate(expected_items):
            for key, value in expected_item.items():
                self.assertEqual(items[index][key], value)


if __name__ == '__main__':
    unittest.main()
