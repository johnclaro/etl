from urllib.parse import urljoin

import requests

import etl


def login():
    url = urljoin(etl.settings.get('load_base'), 'accounts/login')
    credentials = {
        'username': etl.settings.get('username'),
        'password': etl.settings.get('password')
    }
    response = requests.post(url, json=credentials)
    tokens = response.json()
    access = tokens.get('access')
    return access
