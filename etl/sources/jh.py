import datetime
from datetime import timedelta
from urllib.parse import urljoin

import requests
import pandas as pd

from .. import settings


def extract():
    url = 'https://raw.githubusercontent.com/datasets/covid-19/master/data/' \
          'time-series-19-covid-combined.csv'
    df = pd.read_csv(url)
    return df


def transform(df):
    df.columns = df.columns.str.strip().str.lower()
    df['date'] = pd.to_datetime(df['date'])
    columns = {
        '/': '_',
        'confirmed': 'cases',
        'country_region': 'country',
        'province_state': 'state',
        'recovered': 'recoveries'
    }
    for bad_column, good_column in columns.items():
        df.columns = df.columns.str.replace(bad_column, good_column)

    try:
        df = df[df.country == 'Ireland']
    except AttributeError:
        pass

    df = df.drop(columns=['state'])

    if settings.DAYS:
        days = int(settings.DAYS)
        yesterday = datetime.datetime.now() - timedelta(days=days)
        yesterday = yesterday.replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0
        )
        df = df[df.date == yesterday]

    return df


def load(df):
    url = urljoin(settings.URL, 'covid/upsert')
    for index, row in df.iterrows():
        payload = {
            'date': row.date,
            'country': row.country,
            'cases': row.cases,
            'deaths': row.deaths,
            'recoveries': row.recoveries
        }
        requests.post(url, data=payload)


def etl():
    response = extract()
    data = transform(response)
    load(data)
