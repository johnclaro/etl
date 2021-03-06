import json
from datetime import datetime
from urllib.parse import urljoin

import requests

from etl import settings


class HSPC:

    def __init__(
        self,
        date,
        hospitals,
        non_hospitals,
        labs,
        positive_all,
        positive_rate_all,
        test_24,
        test_7,
        positive_7,
        positive_rate_7,
        fid
    ):
        self.date = self.clean_date(date)
        self.hospitals = hospitals
        self.non_hospitals = non_hospitals
        self.labs = labs
        self.positive_all = positive_all
        self.positive_rate_all = positive_rate_all
        self.test_24 = test_24
        self.test_7 = test_7
        self.positive_all = positive_7
        self.positive_rate_7 = positive_rate_7
        self.fid = fid

    def clean_date(self, date):
        date = date / 1000  # Convert unix timestamp in milliseconds to seconds
        date = datetime.fromtimestamp(date)
        date = date.strftime('%Y-%m-%d %H:%M:%S')
        return date


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
        hspc = HSPC(
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
        data.append(hspc.__dict__)

    return data


def load(data):
    url = urljoin(settings.URL, 'swabs/upsert')
    data = json.dumps(data)
    response = requests.post(url, data=data)
    return data


def etl():
    response = extract()
    data = transform(response)
    load(data)
