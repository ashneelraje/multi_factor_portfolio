import pandas as pd

def get_sp500_tickers():
    df = pd.read_csv("data/universe/sp500_constituents.csv", encoding="latin1")
    tickers = df["Symbol"].tolist()
    return tickers