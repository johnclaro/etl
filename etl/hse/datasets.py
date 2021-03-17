from urllib.parse import urljoin

import requests

import etl
from etl import auth
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
            'counties': 'https://services1.arcgis.com/eNO7HHeQ3rUcBllm/'
                        'arcgis/rest/services/Covid19CountyStatisticsHPSC'
                        'IrelandOpenData/FeatureServer/0/query?where='
                        '1%3D1&outFields=*&outSR=4326&f=json',
            'swabs': 'https://services-eu1.arcgis.com/'
                     'z6bHNio59iTqqSUY/arcgis/rest/services/'
                     'LaboratoryLocalTimeSeriesHistoricView/'
                     'FeatureServer/0/query'
                     '?where=1%3D1&outFields=*&outSR=4326&f=json',
        }
        self.dataset = dataset
        self.extract_url = datasets[dataset]
        self.load_url = urljoin(
            etl.settings['load_base'],
            f'covid/hse/{dataset}/upsert'
        )

    def extract(self):
        response = requests.get(self.extract_url).json()
        return response

    def transform(self, response: dict):
        items = []

        # from etl.helpers import hse_convert_fields_for_django
        # hse_convert_fields_for_django(response)

        for index, feature in enumerate(response['features']):
            attributes = feature['attributes']

            if self.dataset == 'swabs':
                pos1 = attributes.get('Positive')
                prate = attributes.get('PRate')
                total_labs = attributes.get('TotalLabs')
                if index:
                    prev_attrs = response['features'][index - 1]['attributes']
                    prev_pos = prev_attrs.get('Positive')
                    prev_labs = prev_attrs.get('TotalLabs')
                    pos1 -= prev_pos
                    prate = (pos1 / (total_labs - prev_labs)) * 100
                    prate = round(prate, 2)
                attributes['pos1'] = pos1
                attributes['posr1'] = prate

            item = Item(**attributes)
            items.append(item.__dict__)
        return items

    def load(self, items: list):
        access = auth.login()
        headers = {'Authorization': f'Bearer {access}'}
        response = requests.post(self.load_url, json=items, headers=headers)
        return response
