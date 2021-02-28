import pandas as pd


def extract(url):
    df = pd.read_csv(url, index_col=0)
    return df


def transform(df):
    df.index = pd.to_datetime(df.index)
    df.columns = df.columns.str.strip().str.lower()
    df.columns = df.columns.str.replace('/', '_')
    return df


def main():
    ny = extract('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv')
    jh = extract('https://raw.githubusercontent.com/datasets/covid-19/master/data/time-series-19-covid-combined.csv')

    jh = transform(jh)
    print(jh)


if __name__ == '__main__':
    main()
