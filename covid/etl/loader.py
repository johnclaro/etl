import urllib
import pickle
import base64
from urllib.parse import urljoin

from covid import settings


def load(df):
    url = urljoin(settings.WEBSITE_URL, 'covid/upsert')
    pickled = pickle.dumps(df)
    df_b64 = base64.b64encode(pickled)
    payload = {'df_b64': df_b64}
    data = urllib.parse.urlencode(payload).encode('utf-8')
    response = urllib.request.urlopen(url, data)
    print(response)
