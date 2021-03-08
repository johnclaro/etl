import datetime
from datetime import timedelta
from urllib.parse import urljoin

import requests
import pandas as pd

import etl
from etl.sources import Source
from .items import Case


class JohnHopkins(Source):

    def __init__(self, dataset):
        datasets = {
            'cases': 'https://raw.githubusercontent.com/datasets/'
                     'covid-19/master/data/time-series-19-covid-combined.csv',
        }
        self.extract_url = datasets[dataset]
        self.load_url = urljoin(
            etl.settings['load_base'],
            f'johnhopkins/{dataset}/upsert'
        )

    def extract(self):
        df = pd.read_csv(self.extract_url)
        return df

    def transform(self, df):
        data = []
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

        time = etl.settings.get('time')
        if time >= 1:
            date = datetime.datetime.now() - timedelta(days=time)
            date = date.replace(hour=0, minute=0, second=0, microsecond=0)
            df = df[df.date == date]

        for _, row in df.iterrows():
            case = Case(
                date=row.date,
                country=row.country,
                cases=row.cases,
                deaths=row.deaths,
                recoveries=row.recoveries
            )
            data.append(case.__dict__)

        return data

    def load(self, items):
        response = requests.post(self.load_url, json=items)
        return response
