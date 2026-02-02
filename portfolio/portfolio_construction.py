import pandas as pd
import numpy as np


def construct_equal_weight_portfolio_with_costs(
    composite_scores: pd.DataFrame,
    prices: pd.DataFrame,
    top_pct: float = 0.20,
    transaction_cost: float = 0.001
):

    dates = composite_scores.index
    tickers = composite_scores.columns

    prev_weights = pd.Series(0.0, index=tickers)

    portfolio_returns = []
    weight_history = []

    for t in range(len(dates) - 1):
        date_t = dates[t]
        date_tp1 = dates[t + 1]

        scores_t = composite_scores.loc[date_t].dropna()

        if scores_t.empty:
            continue

        n_select = int(len(scores_t) * top_pct)
        selected = scores_t.sort_values(ascending=False).iloc[:n_select].index

        weights = pd.Series(0.0, index=tickers)
        weights[selected] = 1.0 / n_select

        price_t = prices.loc[date_t, selected]
        price_tp1 = prices.loc[date_tp1, selected]

        valid = price_t.notna() & price_tp1.notna()
        returns = price_tp1[valid] / price_t[valid] - 1.0
        aligned_weights = weights.loc[returns.index]
        gross_return = (aligned_weights * returns).sum()

        turnover = 0.5 * np.abs(weights - prev_weights).sum()
        cost = transaction_cost * turnover

        net_return = gross_return - cost

        portfolio_returns.append({
            "date": date_tp1,
            "gross_return": gross_return,
            "net_return": net_return,
            "turnover": turnover,
            "transaction_cost": cost
        })

        weight_record = weights.copy()
        weight_record.name = date_tp1
        weight_history.append(weight_record)

        prev_weights = weights.copy()

    portfolio_returns = pd.DataFrame(portfolio_returns).set_index("date")
    portfolio_weights = pd.DataFrame(weight_history)

    return portfolio_returns, portfolio_weights
