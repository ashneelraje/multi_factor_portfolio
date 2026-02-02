import pandas as pd


def construct_equal_weight_benchmark(monthly_prices):
    """
    Equal-weight monthly rebalanced benchmark.
    Forward returns, no transaction costs.
    """

    # Forward returns
    returns = monthly_prices.pct_change().shift(-1)

    benchmark_returns = []

    for date in returns.index[:-1]:
        ret_t = returns.loc[date].dropna()

        if ret_t.empty:
            continue

        weights = 1 / len(ret_t)
        portfolio_return = (ret_t * weights).sum()

        benchmark_returns.append(
            {
                "date": date,
                "benchmark_return": portfolio_return,
            }
        )

    benchmark_returns = pd.DataFrame(benchmark_returns).set_index("date")

    return benchmark_returns
