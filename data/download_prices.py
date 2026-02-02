import yfinance as yf
import pandas as pd

def download_price_data(tickers, start_date, end_date):
    prices = yf.download(
        tickers=tickers,
        start=start_date,
        end=end_date,
        auto_adjust=True,
        progress=False,
        group_by="ticker"
    )

    if isinstance(prices.columns, pd.MultiIndex):
        prices = prices.xs("Close", axis=1, level=1)

    prices = prices.dropna(axis=1, how="all")
    return prices
