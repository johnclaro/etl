import json
import datetime
from datetime import timedelta

import requests
import pandas as pd

from etl import settings
from etl.sources import Source
from etl.covid.johnhopkins.items import Case


class JohnHopkins(Source):

    def __init__(self):
        Source.__init__(self)
        urls = {
            'cases': 'https://raw.githubusercontent.com/datasets/covid-19/master/data/time-series-19-covid-combined.csv',
        }
        self.extract_url = urls[self.dataset]

    def extract(self):
        df = pd.read_csv(self.extract_url)
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

        if settings.TIME >= 1:
            yesterday = datetime.datetime.now() - timedelta(days=settings.TIME)
            yesterday = yesterday.replace(
                hour=0,
                minute=0,
                second=0,
                microsecond=0
            )
            df = df[df.date == yesterday]

        return df

    def load(self, df):
        status = {'successes': 0, 'errors': 0}
        for _, row in df.iterrows():
            case = JohnHopkinsCase(
                date=row.date,
                country=row.country,
                cases=row.cases,
                deaths=row.deaths,
                recoveries=row.recoveries
            )
            data = json.dumps(case.__dict__)
            response = requests.post(self.load_url, data=data)
            if response.status_code == 200:
                status['successes'] += 1
            else:
                status['errors'] += 1
        return status
