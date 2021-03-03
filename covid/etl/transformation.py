import datetime
from datetime import timedelta

import pandas as pd


def clean(df):
    df.columns = df.columns.str.strip().str.lower()
    df['date'] = pd.to_datetime(df['date'])
    columns = {
        '/': '_',
        'confirmed': 'cases',
        'country_region': 'country',
        'province_state': 'state'
    }
    for bad_column, good_column in columns.items():
        df.columns = df.columns.str.replace(bad_column, good_column)
    return df


def filtrate(df, timeset):
    try:
        df = df[df.country == 'Ireland']
    except AttributeError:
        pass

    df = df.drop(columns=['state'])

    if timeset == 'yesterday':
        yesterday = datetime.datetime.now() - timedelta(days=1)
        yesterday = yesterday.replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0
        )
        df = df[df.date == yesterday]

    return df


def join(nyt, jh):
    df = nyt.merge(jh, on='date', suffixes=('_nyt', '_jh'))
    df = df[['date', 'cases_nyt', 'deaths_nyt', 'recovered']]
    df.columns = df.columns.str.replace('cases_nyt', 'cases')
    df.columns = df.columns.str.replace('deaths_nyt', 'deaths')
    return df


def transform(df, timeset):
    df = clean(df)
    df = filtrate(df, timeset)
    return df
