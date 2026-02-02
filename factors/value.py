import pandas as pd
import yfinance as yf

def get_ttm_eps(tickers):
    eps_data = {}
    
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            eps = stock.info.get('trailingEps', None)
            eps_data[ticker] = eps
        except:
            eps_data[ticker] = None
    
    return pd.Series(eps_data)



def compute_value_factor(monthly_prices, eps_series):
    ep = monthly_prices.copy()
    
    for col in ep.columns:
        if col in eps_series.index and eps_series[col] is not None:
            ep[col] = eps_series[col] / ep[col]
        else:
            ep[col] = None
            
    return ep