import json
from urllib.parse import urljoin

import requests

from etl import settings
from etl.models import Swab


def extract():
    url = 'https://services-eu1.arcgis.com/z6bHNio59iTqqSUY/arcgis/' \
          'rest/services/LaboratoryLocalTimeSeriesHistoricView/' \
          'FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=json'
    response = requests.get(url).json()
    return response


def transform(response):
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


def load(data):
    status = {'success': 0, 'error': 0}
    url = urljoin(settings.URL, 'swabs/upsert')
    data = json.dumps(data)
    response = requests.post(url, data=data)
    if response.status_code == 200:
        status['success'] += 1
    else:
        status['error'] += 1
    return status


def etl():
    response = extract()
    data = transform(response)
    status = load(data)
    return status
