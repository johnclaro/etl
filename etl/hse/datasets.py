from urllib.parse import urljoin

import requests

import etl
from etl import auth
from etl.sources import Source
from .items import Item


class HSE(Source):

    def __init__(self):
        self.extract_urls = (
            'https://services1.arcgis.com/eNO7HHeQ3rUcBllm/arcgis/rest/services/CovidStatisticsProfileHPSCIrelandOpenData/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=json',
            'https://services1.arcgis.com/eNO7HHeQ3rUcBllm/arcgis/rest/services/Covid19CountyStatisticsHPSCIrelandOpenData/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=json',
            'https://services-eu1.arcgis.com/z6bHNio59iTqqSUY/arcgis/rest/services/LaboratoryLocalTimeSeriesHistoricView/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=json',
        )

    def extract(self):
        for url in self.extract_urls:
            response = requests.get(url).json()
            yield response

    def transform(self, response: dict):
        items = []

        for index, feature in enumerate(response['features']):
            attributes = feature['attributes']

            if 'Date_HPSC' in attributes.keys():
                pos1 = attributes.get('Positive')
                prate = attributes.get('PRate')
                total_labs = attributes.get('TotalLabs')
                if index:
                    prev_attrs = response['features'][index - 1]['attributes']
                    prev_pos = prev_attrs.get('Positive')
                    prev_labs = prev_attrs.get('TotalLabs')
                    pos1 -= prev_pos
                    prate = (pos1 / (total_labs - prev_labs)) * 100
                    prate = round(prate, 1)
                attributes['pos1'] = pos1
                attributes['posr1'] = prate

            item = Item(**attributes)
            items.append(item.__dict__)
        return items

    def load(self, items: list):
        access = auth.login()
        headers = {'Authorization': f'Bearer {access}'}
        url = urljoin(etl.settings['load_base'], 'covid/hse/upsert')
        response = requests.post(url, json=items, headers=headers)
        return response
