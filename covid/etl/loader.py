import urllib
from urllib.parse import urljoin

from covid import settings


def load(df):
    url = urljoin(settings.WEBSITE_URL, 'covid/upsert')
    upserted = 0
    for index, row in df.iterrows():
        payload = {
            'date': row.date,
            'country': row.country,
            'cases': row.cases,
            'deaths': row.deaths,
            'recoveries': row.recoveries
        }
        data = urllib.parse.urlencode(payload).encode('utf-8')
        request = urllib.request.Request(url, data=data)
        urllib.request.urlopen(request)
        upserted += 1
    return upserted
