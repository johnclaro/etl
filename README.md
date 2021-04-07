# Dags
![Dags](https://github.com/johnclaro/etl/actions/workflows/deploy.yml/badge.svg)

Automated ETLs using Apache Airflow

## Installation

Dags uses Python 3.7.0.
```sh-session
pip install --upgrade pip==20.2.4
pip install -r requirements.txt
```

## Usage

Initialise Airflow
```sh-session
airflow db init
airflow users create --username john --firstname John --lastname Claro --role Admin --email jkrclaro@gmail.com
```

Start Airflow
```
airflow webserver -p 8080 -D && airflow scheduler -D
```

Run tests
```sh-session
python setup.py test
```

## DAGs

Update `airflow/airflow.cfg`
```
dags_folder = ~/etl

load_examples = False
load_default_connections = False
```