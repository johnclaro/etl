from etl.covid.items import Item


class Case(Item):

    def __init__(self, date, country, cases, deaths, recoveries):
        Item.__init__(self, date)
        self.country = country
        self.cases = cases
        self.deaths = deaths
        self.recoveries = recoveries
