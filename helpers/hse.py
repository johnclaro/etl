from datetime import datetime, timedelta

from airflow.utils.dates import days_ago
from airflow.models.taskinstance import TaskInstance

from helpers.common import default_args


dag_args = {
    'dag_id': 'hse',
    'default_args': default_args,
    'schedule_interval': timedelta(days=1),
    'start_date': days_ago(0, 0, 0, 0),
    'description': 'ETLs for HSE',
    'tags': ['hse'],
}


def _clean_date(date):
    try:
        date = datetime.fromtimestamp(date)
    except ValueError:
        date = date / 1000  # Converts unix timestamp in ms to seconds
        date = datetime.fromtimestamp(date)

    date = date.strftime('%Y-%m-%d')
    return date


def transform(ti: TaskInstance, task: str) -> list:
    response = ti.xcom_pull(task_ids=f'extract_{task}', key='response')

    dates = (
        'date',
        'date_hpsc',
        'statisticsprofiledate',
        'timestampdate',
    )
    items = []
    for feature in response['features']:
        item = {}
        attributes = feature['attributes']
        for key, value in attributes.items():
            key = key.lower()
            if key in dates:
                item[key] = _clean_date(value)
            else:
                item[key] = value
        items.append(item)
    ti.xcom_push(key='items', value=items)


def transform_swabs(ti: TaskInstance, task: str) -> list:
    response = ti.xcom_pull(task_ids=f'extract_{task}', key='response')

    dates = (
        'date',
        'date_hpsc',
        'statisticsprofiledate',
        'timestampdate',
    )
    items = []
    for index, feature in enumerate(response['features']):
        item = {}
        attributes = feature['attributes']
        pos1 = attributes.get('Positive')
        prate = attributes.get('PRate')
        total_labs = attributes.get('TotalLabs')
        if index:
            prev_attrs = response['features'][index - 1]['attributes']
            prev_pos = prev_attrs.get('Positive')
            prev_labs = prev_attrs.get('TotalLabs')
            pos1 -= prev_pos
            prate = (pos1 / (total_labs - prev_labs)) * 100
            prate = round(prate, 1)
        attributes['pos1'] = pos1
        attributes['posr1'] = prate
        for key, value in attributes.items():
            key = key.lower()
            if key in dates:
                item[key] = _clean_date(value)
            else:
                item[key] = value
        items.append(item)
    ti.xcom_push(key='items', value=items)
