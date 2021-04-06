import os
from datetime import datetime, timedelta
from urllib.parse import urljoin

from airflow.decorators import dag, task
from airflow.utils.dates import days_ago

import requests


class Item:

    def __init__(self, **kwargs):
        dates = (
            'date',
            'date_hpsc',
            'statisticsprofiledate',
            'timestampdate',
        )
        for key, value in kwargs.items():
            key = key.lower()
            if key in dates:
                value = clean_date(value)
            setattr(self, key.lower(), value)


def clean_date(date):
    try:
        date = datetime.fromtimestamp(date)
    except ValueError:
        # Converts unix timestamp in milliseconds to seconds
        date = date / 1000
        date = datetime.fromtimestamp(date)

    date = date.strftime('%Y-%m-%d')
    return date


args = {
    'default_args': {
        'owner': 'john',
    },
    'schedule_interval': timedelta(minutes=1),
    'start_date': days_ago(0, 0, 0, 0),
    'tags': ['backend'],
}


@dag(**args)
def hse_swabs():

    @task()
    def extract() -> dict:
        url = 'https://services-eu1.arcgis.com/z6bHNio59iTqqSUY/arcgis/rest/services/LaboratoryLocalTimeSeriesHistoricView/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=json'
        response = requests.get(url).json()
        return response

    @task()
    def transform(response: dict) -> list:
        items = []
        for index, feature in enumerate(response['features']):
            attributes = feature['attributes']
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

    @task()
    def load(items: dict):
        credentials = {
            'username': os.getenv('BACKEND_USERNAME', 'guestusername'),
            'password': os.getenv('BACKEND_PASSWORD', 'guestpassword'),
        }
        base = os.getenv('BACKEND_BASE', 'http://localhost:8000')
        auth_url = urljoin(base, 'accounts/login')
        load_url = urljoin(base, 'covid/hse/swabs/upsert')

        response = requests.post(auth_url, json=credentials)
        tokens = response.json()
        access = tokens.get('access')
        headers = {'Authorization': f'Bearer {access}'}
        response = requests.post(load_url, json=items, headers=headers)

    response = extract()
    items = transform(response)
    load(items)


hse_swabs = hse_swabs()
