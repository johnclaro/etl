from enum import Enum


class Dataset(Enum):
    NEW_YORK_TIMES = 'https://raw.githubusercontent.com/nytimes/' \
                     'covid-19-data/master/us.csv'
    JOHN_HOPKINS = 'https://raw.githubusercontent.com/datasets/' \
                   'covid-19/master/data/time-series-19-covid-combined.csv'
