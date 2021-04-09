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


def transform(ti: TaskInstance, task: str) -> None:
    """Transforms HSE JSON data into its JSON Django model equivalent.

    Args:
        ti: Task instance from a dag
        task: Name of an HSE task, e.g. cases, swabs, counties

    Returns:
        None but data is pushed through XCom
    """
    response = ti.xcom_pull(task_ids='extract', key='response')

    dates = (
        'date',
        'date_hpsc',
        'statisticsprofiledate',
        'timestampdate',
    )
    items = []
    for index, feature in enumerate(response['features']):
        item = {}
        attrs = feature['attributes']

        if task == 'swabs':
            if index:
                prev_attrs = response['features'][index - 1]['attributes']
            attrs = _calculate_daily_swabs(attrs, prev_attrs)

        for key, value in attrs.items():
            key = key.lower()
            if key in dates:
                item[key] = _clean_date(value)
            else:
                item[key] = value
        items.append(item)

    ti.xcom_push(key='items', value=items)


def _clean_date(date: int) -> str:
    """Converts a unix timestamp into its date string equivalent.

    Args:
        date: Unix timestamp

    Returns:
        A date in YYYY-MM-DD format
    """
    try:
        date = datetime.fromtimestamp(date)
    except ValueError:
        date = date / 1000  # Converts unix timestamp in ms to seconds
        date = datetime.fromtimestamp(date)

    date = date.strftime('%Y-%m-%d')
    return date


def _calculate_daily_swabs(attrs: dict, prev_attrs: dict = None) -> dict:
    """Calculates the daily value of swabs.

    Args:
        attrs: Current attributes of HSE data
        prev_attrs: Previous attributes of HSE data

    Returns:
        Updated attrs dict with newly added "pos1" and "posr1" key values
    """
    pos1 = attrs['Positive']
    prate = attrs['Prate']
    total_labs = attrs['TotalLabs']
    if prev_attrs:
        prev_pos = prev_attrs['Positive']
        prev_labs = prev_attrs['TotalLabs']
        pos1 -= prev_pos
        prate = (pos1 / (total_labs - prev_labs)) * 100
        prate = round(prate, 1)
    attrs['pos1'] = pos1
    attrs['posr1'] = prate
    return attrs
