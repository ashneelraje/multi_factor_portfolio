import numpy as np
import pandas as pd

def annualized_return(returns, periods_per_year=12):
    return (1 + returns.mean()) ** periods_per_year - 1

def annualized_volatility(returns, periods_per_year=12):
    return returns.std() * np.sqrt(periods_per_year)

def sharpe_ratio(returns, risk_free_rate=0.0, periods_per_year=12):
    excess = returns - risk_free_rate / periods_per_year
    return excess.mean() / excess.std() * np.sqrt(periods_per_year)

def max_drawdown(returns):
    cumulative = (1 + returns).cumprod()
    peak = cumulative.cummax()
    drawdown = (cumulative - peak) / peak
    return drawdown.min()
