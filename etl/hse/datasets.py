from urllib.parse import urljoin

import requests

import etl
from etl.sources import Source
from .items import Item


class HSE(Source):

    def __init__(self, dataset):
        datasets = {
            'cases': 'https://services1.arcgis.com/eNO7HHeQ3rUcBllm/'
                     'arcgis/rest/services/'
                     'CovidStatisticsProfileHPSCIrelandOpenData/'
                     'FeatureServer/0/query'
                     '?where=1%3D1&outFields=*&outSR=4326&f=json',
            'counties': 'https://services1.arcgis.com/eNO7HHeQ3rUcBllm/' \
                        'arcgis/rest/services/Covid19CountyStatisticsHPSC' \
                        'IrelandOpenData/FeatureServer/0/query?where=' \
                        '1%3D1&outFields=*&outSR=4326&f=json',
            'swabs': 'https://services-eu1.arcgis.com/'
                     'z6bHNio59iTqqSUY/arcgis/rest/services/'
                     'LaboratoryLocalTimeSeriesHistoricView/'
                     'FeatureServer/0/query'
                     '?where=1%3D1&outFields=*&outSR=4326&f=json',
        }
        self.extract_url = datasets[dataset]
        self.load_url = urljoin(
            etl.settings['load_base'],
            f'hse/{dataset}/upsert'
        )

    def extract(self):
        response = requests.get(self.extract_url).json()
        return response

    def transform(self, response: dict):
        items = []

        # from etl.helpers import hse_convert_fields_for_django
        # hse_convert_fields_for_django(response)

        for feature in response['features']:
            attributes = feature['attributes']
            item = Item(**attributes)
            items.append(item.__dict__)
        return items

    def load(self, items: list):
        response = requests.post(self.load_url, json=items)
        return response
