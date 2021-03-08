import json
from urllib.parse import urljoin

import requests

from etl import settings
from etl.sources import Source
from etl.covid.hse.items import Swab, Case


class HSE(Source):

    def __init__(self):
        Source.__init__(self)
        urls = {
            'cases': 'https://services1.arcgis.com/eNO7HHeQ3rUcBllm/arcgis/rest/services/CovidStatisticsProfileHPSCIrelandOpenData/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=json',
            'swabs': 'https://services-eu1.arcgis.com/z6bHNio59iTqqSUY/arcgis/rest/services/LaboratoryLocalTimeSeriesHistoricView/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=json',
        }
        self.extract_url = urls[self.dataset]
        load_url = urljoin(settings.URL, f'covid/hse/{self.dataset}/upsert')
        self.load_url = load_url

    def extract(self):
        response = requests.get(self.extract_url).json()
        return response

    def transform(self, response):
        data = []
        for feature in response['features']:
            attribute = feature['attributes']
            if self.dataset == 'cases':
                item = Case(**attribute)
            elif self.dataset == 'swabs':
                item = Swab(**attribute)
            data.append(item.__dict__)
        return data

    def load(self, data):
        status = {'successes': 0, 'errors': 0}
        data = json.dumps(data, indent=4, sort_keys=True)
        print(data)
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        response = requests.post(self.load_url, data=data, headers=headers)
        print(response.json())
        if response.status_code == 200:
            status['successes'] += 1
        else:
            status['errors'] += 1
        return status
