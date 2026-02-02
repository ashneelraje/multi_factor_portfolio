import yfinance as yf
import pandas as pd
import time

def fetch_market_cap(tickers, sleep_time=0.3):
    
    market_caps = {}

    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            market_caps[ticker] = stock.info.get("marketCap", None)
        except Exception:
            market_caps[ticker] = None

        time.sleep(sleep_time)

    market_cap_series = pd.Series(market_caps)
    market_cap_series.name = "market_cap"
    
    return market_cap_series