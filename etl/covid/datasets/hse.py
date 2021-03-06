import json
from urllib.parse import urljoin

import requests

from etl import settings
from etl.sources import Source
from etl.covid.items import Swab


class HSE(Source):

    def __init__(self, dataset):
        self.dataset = dataset

    def extract(self):
        urls = {
            'cases': 'https://services1.arcgis.com/eNO7HHeQ3rUcBllm/arcgis/rest/services/CovidStatisticsProfileHPSCIrelandOpenData/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=json',
            'swabs': 'https://services-eu1.arcgis.com/z6bHNio59iTqqSUY/arcgis/rest/services/LaboratoryLocalTimeSeriesHistoricView/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=json',
        }
        url = urls[self.dataset]
        response = requests.get(url).json()
        return response

    def transform(self, response):
        functions = {
            'cases': self._transform_cases(response),
            'swabs': self._transform_swabs(response)
        }
        data = functions[self.dataset]
        return data

    def load(self, data):
        status = {'successes': 0, 'errors': 0}
        url = urljoin(settings.URL, 'swabs/upsert')
        data = json.dumps(data)
        response = requests.post(url, data=data)
        if response.status_code == 200:
            status['successes'] += 1
        else:
            status['errors'] += 1
        return status

    def _transform_cases(self, response):
        data = []
        return data

    def _transform_swabs(self, response):
        data = []
        for feature in response['features']:
            attribute = feature['attributes']
            swab = Swab(
                date=attribute['Date_HPSC'],
                hospitals=attribute['Hospitals'],
                non_hospitals=attribute['NonHospitals'],
                labs=attribute['TotalLabs'],
                positive_all=attribute['Positive'],
                positive_rate_all=attribute['PRate'],
                test_24=attribute['Test24'],
                test_7=attribute['Test7'],
                positive_7=attribute['Pos7'],
                positive_rate_7=attribute['PosR7'],
                fid=attribute['FID']
            )
            data.append(swab.__dict__)

        return data
