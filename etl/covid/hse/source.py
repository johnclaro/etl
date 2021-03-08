import json
from urllib.parse import urljoin

import requests

from etl import settings
from etl.sources import Source
from .items import Item


class HSE(Source):

    def __init__(self):
        Source.__init__(self)
        urls = {
            'cases': 'https://services1.arcgis.com/eNO7HHeQ3rUcBllm/arcgis/rest/services/CovidStatisticsProfileHPSCIrelandOpenData/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=json',
            'swabs': 'https://services-eu1.arcgis.com/z6bHNio59iTqqSUY/arcgis/rest/services/LaboratoryLocalTimeSeriesHistoricView/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=json',
        }
        self.extract_url = urls[self.dataset]
        self.load_url = urljoin(
            settings.URL,
            f'covid/hse/{self.dataset}/upsert'
        )

    def extract(self):
        response = requests.get(self.extract_url).json()
        return response

    def transform(self, response):
        items = []
        for feature in response['features']:
            attributes = feature['attributes']
            item = Item(**attributes)
            items.append(item.__dict__)
        return items

    def load(self, items):
        status = {'successes': 0, 'errors': 0}
        response = requests.post(self.load_url, json=items)
        if response.status_code == 200:
            status['successes'] += 1
        else:
            status['errors'] += 1
        return status
