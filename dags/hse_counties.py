from datetime import datetime, timedelta
from urllib.parse import urljoin

from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
from airflow.models import Variable

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
    'tags': ['hse'],
}


@dag(**args)
def hse_counties():

    @task()
    def extract() -> dict:
        url = 'https://services1.arcgis.com/eNO7HHeQ3rUcBllm/arcgis/rest/' \
              'services/Covid19CountyStatisticsHPSCIrelandOpenData/' \
              'FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=json'
        response = requests.get(url).json()
        return response

    @task()
    def transform(response: dict) -> list:
        items = []
        for feature in response['features']:
            attributes = feature['attributes']
            item = Item(**attributes)
            items.append(item.__dict__)
        return items

    @task()
    def load(items: dict):
        credentials = {
            'username': Variable.get('BACKEND_USERNAME', default_var='guestusername'),
            'password': Variable.get('BACKEND_PASSWORD', default_var='guestpassword'),
        }
        base = Variable.get('BACKEND_BASE', default_var='http://localhost:8000')
        auth_url = urljoin(base, 'accounts/login')
        load_url = urljoin(base, 'hse/counties/upsert')
        response = requests.post(auth_url, json=credentials)
        if response.status_code != 200:
            raise ValueError('Status code was not 200')

        access = response.json().tokens.get('access')
        headers = {'Authorization': f'Bearer {access}'}
        response = requests.post(load_url, json=items, headers=headers)

        if response.status_code != 200:
            raise ValueError('Status code was not 200')

    response = extract()
    items = transform(response)
    load(items)


hse_counties = hse_counties()
