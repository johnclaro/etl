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

Must include `requests` and `pandas`

```sh-session
zip -r9 layers/etl.zip layers
```