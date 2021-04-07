# Dags
![Dags](https://github.com/johnclaro/etl/actions/workflows/deploy.yml/badge.svg)

Automated ETLs using Apache Airflow

## Installation

Dags uses **Python 3.7.0**.
```console
pip install --upgrade pip==20.2.4
pip install -r requirements.txt
```

## Usage

Initialise Airflow
```console
airflow db init
airflow users create --username john --firstname John --lastname Claro --role Admin --email jkrclaro@gmail.com
```

Start Airflow
```console
airflow webserver -p 8080 -D && airflow scheduler -D
```

## DAGs

Update **airflow/airflow.cfg**
```ini
dags_folder = ~/dags/dags
load_examples = False
load_default_connections = False
default_ui_timezone = Europe/Dublin
default_timezone = Europe/Dublin
```