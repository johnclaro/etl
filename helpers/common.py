from datetime import timedelta
from urllib.parse import urljoin

from airflow.models import Variable
from airflow.models.taskinstance import TaskInstance

import requests


default_args = {
    'owner': 'john',
    'depends_on_past': False,
    'email': ['jkrclaro@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}


def extract(ti: TaskInstance, url: str) -> dict:
    """Sends an HTTP GET request to extract JSON data.

    Args:
        ti: Task instance of a dag
        url: URL to be extracted

    Returns:
        None but data is pushed through XCom
    """
    response = requests.get(url).json()
    ti.xcom_push(key='response', value=response)


def load(ti: TaskInstance, task: str) -> None:
    """Sends an HTTP POST request to backend with newly transformed COVID data.

    It first authenticates by logging in to get the JWT access token.
    Sets access token to header of the next request for uploading COVID data.

    Args:
        ti: Task instance of a dag
        task:  Name of an HSE task, e.g. cases, swabs, counties

    Returns:
        None
    """
    url = f'hse/{task}/upsert'
    items = ti.xcom_pull(task_ids='transform', key='items')

    username = Variable.get('BACKEND_USERNAME', default_var='guestusername')
    password = Variable.get('BACKEND_PASSWORD', default_var='guestpassword')
    credentials = {
        'username': username,
        'password': password,
    }
    base = Variable.get('BACKEND_BASE', default_var='http://localhost:8000')
    auth_url = urljoin(base, 'accounts/login')
    response = requests.post(auth_url, json=credentials)

    if response.status_code != 200:
        raise Exception(f'Backend server returned {response.status_code}')

    access = response.json().get('access')
    headers = {'Authorization': f'Bearer {access}'}
    load_url = urljoin(base, url)
    response = requests.post(load_url, json=items, headers=headers)

    if response.status_code != 200:
        raise Exception(f'Backend server returned {response.status_code}')
