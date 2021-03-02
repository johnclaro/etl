import urllib
from urllib.parse import urljoin

import settings


def load(df):
    payload = {
        'date': df.iloc[0]['date'],
        'cases': df.iloc[0]['cases'],
        'deaths': df.iloc[0]['deaths'],
        'recovered': df.iloc[0]['recovered']
    }
    url = urljoin(settings.WEBSITE_URL, 'covid/upsert')
    print(url)

    data = urllib.parse.urlencode(payload).encode('ascii')
    response = urllib.request.urlopen(url, data)
    print(response.read())
