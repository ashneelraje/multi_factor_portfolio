import yfinance as yf
import pandas as pd

def get_spy_returns(start_date, end_date):
    spy = yf.download(
        "SPY",
        start=start_date,
        end=end_date,
        auto_adjust=True,
        progress=False
    )["Close"]

    monthly_prices = spy.resample("ME").last()
    returns = monthly_prices.pct_change().dropna()
    returns.name = "SPY"
    return returns
