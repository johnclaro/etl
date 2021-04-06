# ETL
![ETL](https://github.com/johnclaro/etl/actions/workflows/main.yml/badge.svg)

Run and manage ETLs using Apache Airflow

## Installation

ETL uses Python 3.7.0.
```sh-session
# Use pip 20.2.4 to ensure Apache Airflow installation has no errors
pip install --upgrade pip==20.2.4
pip install -r requirements.txt
```

## Usage

Installing the CLI provides access to the `etl` command.
```sh-session
etl [command]

# Run `-h` for detailed information about commands
etl -h
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