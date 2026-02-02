import yfinance as yf
import pandas as pd
import time

def fetch_roe(tickers, sleep_time=0.3):
   
    roe_data = {}

    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            roe = stock.info.get("returnOnEquity", None)
            roe_data[ticker] = roe
        except Exception:
            roe_data[ticker] = None

        time.sleep(sleep_time) 

    roe_series = pd.Series(roe_data)
    roe_series.name = "roe"

    return roe_series
