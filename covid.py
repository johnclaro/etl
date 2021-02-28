import pandas as pd


def extract(url):
    df = pd.read_csv(url)
    return df


def transform(df):
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

    try:
        df = df[df.country == 'US']
    except AttributeError:
        pass

    return df


def combine(ny, jh):
    df = ny.merge(jh, on='date', suffixes=('_ny', '_jh'))
    df = df[['date', 'cases_ny', 'deaths_ny', 'recovered']]
    df.columns = df.columns.str.replace('cases_ny', 'cases')
    df.columns = df.columns.str.replace('deaths_ny', 'deaths')
    return df


def main():
    ny = extract('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv')
    jh = extract('https://raw.githubusercontent.com/datasets/covid-19/master/data/time-series-19-covid-combined.csv')

    ny = transform(ny)
    jh = transform(jh)

    df = combine(ny, jh)


if __name__ == '__main__':
    main()
