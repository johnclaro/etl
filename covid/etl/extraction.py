import pandas as pd


def extract_csv(url):
    df = pd.read_csv(url)
    return df
