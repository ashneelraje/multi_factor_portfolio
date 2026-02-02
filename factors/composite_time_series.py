import pandas as pd
import numpy as np
from scipy.stats import zscore


def compute_composite_scores(
    momentum_df: pd.DataFrame,
    value_df: pd.DataFrame,
    size_scores: pd.Series,
    quality_scores: pd.Series
) -> pd.DataFrame:

    momentum_df = momentum_df.copy()
    value_df = value_df.copy()

    momentum_df.index = pd.to_datetime(momentum_df.index)
    value_df.index = pd.to_datetime(value_df.index)

    composite_df = pd.DataFrame(
        index=momentum_df.index,
        columns=momentum_df.columns,
        dtype=float
    )

    for date in momentum_df.index:

        if date not in value_df.index:
            continue

        momentum_row = momentum_df.loc[date]
        value_row = value_df.loc[date]

        temp = pd.DataFrame({
            "momentum": momentum_row,
            "value": value_row,
            "size": size_scores,
            "quality": quality_scores
        })

        temp = temp.dropna(how="all")

        if temp.empty:
            continue

        zscores = temp.apply(
            lambda x: zscore(x, nan_policy="omit"),
            axis=0
        )

        composite_row = zscores.mean(axis=1)

        composite_df.loc[date, composite_row.index] = composite_row

    return composite_df


import pandas as pd
import numpy as np


def compute_factor_returns(
    factor_scores: pd.DataFrame,
    monthly_prices: pd.DataFrame,
    quantile: float = 0.2
):

    common_dates = factor_scores.index.intersection(monthly_prices.index)
    common_tickers = factor_scores.columns.intersection(monthly_prices.columns)

    scores = factor_scores.loc[common_dates, common_tickers]
    prices = monthly_prices.loc[common_dates, common_tickers]

    forward_returns = prices.pct_change().shift(-1)

    factor_returns = []

    for date in scores.index[:-1]:
        scores_t = scores.loc[date].dropna()

        if scores_t.empty:
            factor_returns.append(np.nan)
            continue

        ranked = scores_t.sort_values(ascending=False)

        q = int(len(ranked) * quantile)
        if q == 0:
            factor_returns.append(np.nan)
            continue

        long = ranked.iloc[:q].index
        short = ranked.iloc[-q:].index

        long_ret = forward_returns.loc[date, long].mean()
        short_ret = forward_returns.loc[date, short].mean()

        factor_returns.append(long_ret - short_ret)

    return pd.Series(factor_returns, index=scores.index[:-1])


def expand_static_factor(
    factor_series: pd.Series,
    dates: pd.Index
):

    return pd.DataFrame(
        np.tile(factor_series.values, (len(dates), 1)),
        index=dates,
        columns=factor_series.index
    )
