import pytest

from helpers.hse import _clean_date, _calculate_daily_swabs, update_dag_args


@pytest.fixture
def attrs():
    return {
        'Positive': 1,
        'Prate': 1,
        'TotalLabs': 1,
    }


def test_should_pass_cleaning_date_with_unix_timestamp():
    date = _clean_date(1583193600000)
    assert '2020-03-03' == date


def test_should_pass_when_calculating_daily_swabs_with_no_previous_attributes(attrs: dict):
    assert (1, 1) == _calculate_daily_swabs(attrs)


def test_should_pass_when_calculating_daily_swabs_with_different_previous_attributes(attrs: dict):
    prev_attrs = {
        'Positive': 2,
        'TotalLabs': 2,
    }
    assert (-1, 100.0) == _calculate_daily_swabs(attrs, prev_attrs)


def test_should_pass_when_calculating_daily_swabs_with_same_previous_attributes(attrs: dict):
    prev_attrs = {
        'Positive': 1,
        'TotalLabs': 1,
    }
    assert (0, 0) == _calculate_daily_swabs(attrs, prev_attrs)


def test_should_pass_when_updating_dag_args():
    task = 'cases'
    output = update_dag_args(task)
    assert 'hse_cases' == output['dag_id']
    assert 'ETL for HSE cases' == output['description']

# flake8: noqa
