import pandas as pd


def website(url):
    df = pd.read_csv(url)
    return df
