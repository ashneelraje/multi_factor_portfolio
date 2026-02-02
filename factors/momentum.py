import pandas as pd

def compute_momentum(monthly_prices, lookback=12, skip=1):
       
    shifted_prices = monthly_prices.shift(skip)
    momentum = shifted_prices.pct_change(lookback)
    
    return momentum.dropna(how='all')


def zscore_cross_sectional(df):
    return (df - df.mean(axis=1).values.reshape(-1, 1)) / \
           df.std(axis=1).values.reshape(-1, 1)