from datetime import timedelta

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago


default_args = {
    'owner': 'john',
    'depends_on_past': False,
    'start_date': days_ago(0, 0, 0, 0),
    'email': ['jkrclaro@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

dag = DAG(
    'covid19ireland',
    default_args=default_args,
    description="Ireland's COVID-19 Data Hub",
    schedule_interval=timedelta(minutes=1),
)


def cases():
    print('Performing ETL on Cases')


run_etl = PythonOperator(
    task_id='cases',
    python_callable=cases,
    dag=dag,
)

run_etl
