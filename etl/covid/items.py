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
