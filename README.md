# Dags
![Deploy](https://github.com/johnclaro/etl/actions/workflows/deploy.yml/badge.svg)
[![Test](https://github.com/johnclaro/dags/actions/workflows/test.yml/badge.svg)](https://github.com/johnclaro/dags/actions/workflows/test.yml)

Automated ETLs using Apache Airflow

## Installation

[Virtualenv](https://virtualenv.pypa.io/en/latest/) is recommended.

```console
# python3.7
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
export PYTHONPATH=~/dags
airflow webserver -p 8080 -D && airflow scheduler -D
```

## DAGs

Update `airflow/airflow.cfg`
```ini
dags_folder = ~/dags/dags
load_examples = False
load_default_connections = False
default_ui_timezone = Europe/Dublin
default_timezone = Europe/Dublin
```