import json

import requests

from etl.sources import Source
from etl.covid.items import Swab


class HSE(Source):

    def __init__(self):
        Source.__init__(self)
        urls = {
            'cases': 'https://services1.arcgis.com/eNO7HHeQ3rUcBllm/arcgis/rest/services/CovidStatisticsProfileHPSCIrelandOpenData/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=json',
            'swabs': 'https://services-eu1.arcgis.com/z6bHNio59iTqqSUY/arcgis/rest/services/LaboratoryLocalTimeSeriesHistoricView/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=json',
        }
        self.extract_url = urls[self.dataset]

    def extract(self):
        response = requests.get(self.extract_url).json()
        return response

    def transform(self, response):
        if self.dataset == 'cases':
            data = self._transform_cases(response)
        elif self.dataset == 'swabs':
            data = self._transform_swabs(response)
        return data

    def load(self, data):
        status = {'successes': 0, 'errors': 0}
        data = json.dumps(data)
        response = requests.post(self.load_url, data=data)
        if response.status_code == 200:
            status['successes'] += 1
        else:
            status['errors'] += 1
        return status

    def _transform_cases(self, response):
        data = []
        for field in response['fields']:
            print(field['Name'])
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
