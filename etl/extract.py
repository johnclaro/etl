import pandas as pd


def csv(url):
    df = pd.read_csv(url)
    return df
