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


def filtrate(df):
    try:
        df = df[df.country == 'US']
    except AttributeError:
        pass

    return df


def join(nyt, jh):
    df = nyt.merge(jh, on='date', suffixes=('_nyt', '_jh'))
    df = df[['date', 'cases_nyt', 'deaths_nyt', 'recovered']]
    df.columns = df.columns.str.replace('cases_nyt', 'cases')
    df.columns = df.columns.str.replace('deaths_nyt', 'deaths')
    return df


def transform(df):
    df = clean(df)
    df = filtrate(df)
    return df
