from airflow.models import DAG
from airflow.operators.python import PythonOperator

from helpers.common import extract, load
from helpers.hse import transform, dag_args

task = 'counties'
url = 'https://services1.arcgis.com/eNO7HHeQ3rUcBllm/arcgis/rest/services/Covid19CountyStatisticsHPSCIrelandOpenData/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=json'
dag_args['dag_id'] += f'_{task}'
dag_args['description'] += f' {task}'


with DAG(**dag_args) as dag:
    extract_task = PythonOperator(
        task_id=f'extract_{task}',
        python_callable=extract,
        op_kwargs={'url': url},
    )

    transform_task = PythonOperator(
        task_id=f'transform_{task}',
        python_callable=transform,
        op_kwargs={'task': task},
    )

    load_task = PythonOperator(
        task_id=f'load_{task}',
        python_callable=load,
        op_kwargs={'task': task},
    )

    extract_task >> transform_task >> load_task
