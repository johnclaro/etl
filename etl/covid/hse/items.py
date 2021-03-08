
from etl.covid.items import Item


class Swab(Item):

    def __init__(self, **kwargs):
        date = kwargs.pop('Date_HSPC')
        Item.__init__(self, date)
        for key, value in kwargs.items():
            setattr(self, key.lower(), value)


class Case(Item):

    def __init__(self, **kwargs):
        date = kwargs.pop('Date')
        Item.__init__(self, date)
        for key, value in kwargs.items():
            setattr(self, key.lower(), value)
