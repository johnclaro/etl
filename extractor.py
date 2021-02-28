import pandas as pd


def extract(url):
    df = pd.read_csv(url)
    return df
