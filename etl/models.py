import json
from datetime import datetime

import pandas


class Item:

    def __init__(self, date):
        self.date = self.clean_date(date)

    def clean_date(self, date):
        if isinstance(date, pandas._libs.tslibs.timestamps.Timestamp):
            date = date.date()
        elif isinstance(date, int):
            try:
                date = datetime.fromtimestamp(date)
            except ValueError:
                # Converts unix timestamp in milliseconds to seconds
                date = date / 1000
                date = datetime.fromtimestamp(date)

        date = date.strftime('%Y-%m-%d %H:%M:%S')
        return date


class Case(Item):

    def __init__(self, date, country, cases, deaths, recoveries):
        Item.__init__(self, date)
        self.country = country
        self.cases = cases
        self.deaths = deaths
        self.recoveries = recoveries


class Swab(Item):

    def __init__(
        self,
        date,
        hospitals,
        non_hospitals,
        labs,
        positive_all,
        positive_rate_all,
        test_24,
        test_7,
        positive_7,
        positive_rate_7,
        fid
    ):
        Item.__init__(self, date)
        self.hospitals = hospitals
        self.non_hospitals = non_hospitals
        self.labs = labs
        self.positive_all = positive_all
        self.positive_rate_all = positive_rate_all
        self.test_24 = test_24
        self.test_7 = test_7
        self.positive_all = positive_7
        self.positive_rate_7 = positive_rate_7
        self.fid = fid
