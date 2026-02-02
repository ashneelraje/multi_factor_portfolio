import numpy as np
import pandas as pd


def compute_cagr(returns, periods_per_year=12):
    cumulative = (1 + returns).prod()
    n_periods = returns.shape[0]
    return cumulative ** (periods_per_year / n_periods) - 1


def compute_volatility(returns, periods_per_year=12):
    return returns.std() * np.sqrt(periods_per_year)


def compute_sharpe(returns, risk_free_rate=0.0, periods_per_year=12):
    excess = returns - risk_free_rate / periods_per_year
    return excess.mean() / excess.std() * np.sqrt(periods_per_year)


def compute_max_drawdown(cumulative_returns):
    running_max = cumulative_returns.cummax()
    drawdown = cumulative_returns / running_max - 1
    return drawdown.min()


def portfolio_vs_benchmark(returns):
    cumulative_returns = (1 + returns).cumprod()

    return {
        "CAGR": compute_cagr(returns),
        "Volatility": compute_volatility(returns),
        "Sharpe": compute_sharpe(returns),
        "Max Drawdown": compute_max_drawdown(cumulative_returns),
        "Total Return": cumulative_returns.iloc[-1] - 1,
    }
