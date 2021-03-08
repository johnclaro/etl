import pandas


class Case:

    def __init__(self, date, country, cases, deaths, recoveries):
        self.date = clean_date(date)
        self.country = country
        self.cases = cases
        self.deaths = deaths
        self.recoveries = recoveries


def clean_date(date):
    if isinstance(date, pandas._libs.tslibs.timestamps.Timestamp):
        date = date.date()

    date = date.strftime('%Y-%m-%d')
    return date
