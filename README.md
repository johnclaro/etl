# ETL
![ETL](https://github.com/johnclaro/etl/actions/workflows/main.yml/badge.svg)

ETL for Covid data

## Installation

ETL uses Python 3.7.0.
```sh-session
pip install -e .
```

## Usage

Installing the CLI provides access to the `etl` command.
```sh-session
etl [command]

# Run `--help` for detailed information about commands
etl [command] -h
```

## Layers

ETL requires `requests` and `pandas` dependencies for AWS Lambda

**requests**

```sh-session
mkdir -p layers/requests/python/lib/python3.7/site-packages
pip install requests -t layers/python/lib/python3.7/site-packages
zip -r9 requests.zip layers/requests/python
```

**pandas**

Download [pandas-1.0.3-cp37-cp37m-manylinux1_x86_64.whl](https://pypi.org/project/pandas/#files)
and [pytz-2019.3-py2.py3-none-any.whl](https://pypi.org/project/pytz/#files)

```sh-session
# pandas
mkdir -p layers/pandas/python/lib/python3.7/site-packages
unzip pandas-1.0.3-cp37-cp37m-manylinux1_x86_64.whl
mv pandas/ layers/pandas/python/lib/python3.7/site-packages
mv pandas-1.2.2.dist-info/ layers/pandas/python/lib/python3.7/site-packages

# pytz
unzip pytz-2019.3-py2.py3-none-any.whl
mv pytz/ layers/pandas/python/lib/python3.7/site-packages
mv pytz-2021.1.dist-info/ layers/pandas/python/lib/python3.7/site-packages

zip -r9 pandas.zip layers/pandas/python
```