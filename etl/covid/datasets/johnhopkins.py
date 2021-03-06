import json
import datetime
from datetime import timedelta
from urllib.parse import urljoin

import requests
import pandas as pd

from etl import settings
from etl.sources import Source
from etl.covid.items import Case


class JohnHopkins(Source):

    def __init__(self, dataset):
        self.dataset = dataset

    def extract(self):
        url = 'https://raw.githubusercontent.com/datasets/covid-19/master/data/time-series-19-covid-combined.csv'
        df = pd.read_csv(url)
        return df

    def transform(self, df):
        df.columns = df.columns.str.strip().str.lower()
        df['date'] = pd.to_datetime(df['date'])
        columns = {
            '/': '_',
            'confirmed': 'cases',
            'country_region': 'country',
            'province_state': 'state',
            'recovered': 'recoveries'
        }
        for old_column, new_column in columns.items():
            df.columns = df.columns.str.replace(old_column, new_column)

        try:
            df = df[df.country == 'Ireland']
        except AttributeError:
            pass

        df = df.drop(columns=['state'])

        if settings.TIME:
            yesterday = datetime.datetime.now() - timedelta(days=settings.TIME)
            yesterday = yesterday.replace(
                hour=0,
                minute=0,
                second=0,
                microsecond=0
            )
            df = df[df.date == yesterday]

        return df

    def load(self, data):
        url = urljoin(settings.URL, f'covid/{self.dataset}/upsert')
        status = {'success': 0, 'error': 0}

        for _, row in data.iterrows():
            case = Case(
                date=row.date,
                country=row.country,
                cases=row.cases,
                deaths=row.deaths,
                recoveries=row.recoveries
            )
            data = json.dumps(case.__dict__)
            response = requests.post(url, data=data)
            if response.status_code == 200:
                status['success'] += 1
            else:
                status['error'] += 1
        return status
