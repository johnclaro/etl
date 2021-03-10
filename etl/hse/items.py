from datetime import datetime


class Item:

    def __init__(self, **kwargs):
        dates = (
            'date',
            'date_hpsc',
            'statisticsprofiledate',
            'timestampdate',
        )
        for key, value in kwargs.items():
            key = key.lower()
            if key in dates:
                value = clean_date(value)
            setattr(self, key.lower(), value)


def clean_date(date):
    try:
        date = datetime.fromtimestamp(date)
    except ValueError:
        # Converts unix timestamp in milliseconds to seconds
        date = date / 1000
        date = datetime.fromtimestamp(date)

    date = date.strftime('%Y-%m-%d')
    return date
