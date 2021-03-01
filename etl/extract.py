import pandas as pd


def new_york_times():
    url = 'https://raw.githubusercontent.com/nytimes/' \
          'covid-19-data/master/us.csv'
    df = pd.read_csv(url)
    return df


def john_hopkins():
    url = 'https://raw.githubusercontent.com/datasets/covid-19/master/' \
          'data/time-series-19-covid-combined.csv'
    df = pd.read_csv(url)
    return df
