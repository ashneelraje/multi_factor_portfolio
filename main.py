import pandas as pd

from analytics.performance_metrics import portfolio_vs_benchmark
from analytics.factor_attribution import factor_attribution
from analytics.alpha_decomposition import alpha_decomposition

from data.get_sp500_tickers import get_sp500_tickers
from data.download_prices import download_price_data
from data.market_cap import fetch_market_cap
from data.quality_data import fetch_roe

from factors.momentum import compute_momentum, zscore_cross_sectional
from factors.value import get_ttm_eps, compute_value_factor
from factors.size import compute_size_scores
from factors.quality import compute_quality_scores
from factors.composite_time_series import compute_composite_scores, compute_factor_returns, expand_static_factor

from portfolio.portfolio_construction import construct_equal_weight_portfolio_with_costs
from portfolio.benchmark import construct_equal_weight_benchmark

from performance.metrics import annualized_return, annualized_volatility, sharpe_ratio, max_drawdown
from performance.benchmark import get_spy_returns

START_DATE = "2010-01-01"
END_DATE = "2024-01-01"


def main():
    tickers = get_sp500_tickers()

    eps_series = get_ttm_eps(tickers)
    roe = fetch_roe(tickers)
    market_cap = fetch_market_cap(tickers)

    prices = download_price_data(tickers, START_DATE, END_DATE)
    min_obs = int(0.8 * prices.shape[0])
    prices = prices.dropna(axis=1, thresh=min_obs)
    valid_tickers = prices.columns.tolist()
    tickers = valid_tickers

    eps_series = eps_series.loc[eps_series.index.intersection(tickers)]
    roe = roe.loc[roe.index.intersection(tickers)]
    market_cap = market_cap.loc[market_cap.index.intersection(tickers)]

    pd.Series(tickers, name="ticker").to_csv(
        "data/processed/eligible_universe.csv",
        index=False
    )

    monthly_prices = prices.resample("ME").last()
    monthly_prices.to_csv("data/processed/monthly_prices.csv")

    momentum_raw = compute_momentum(monthly_prices)
    momentum_z = zscore_cross_sectional(momentum_raw)
    momentum_z = momentum_z.shift(1)

    value_raw = compute_value_factor(monthly_prices, eps_series)
    value_z = zscore_cross_sectional(value_raw)
    value_z = value_z.shift(1)

    size_scores = compute_size_scores(market_cap)
    quality_scores = compute_quality_scores(roe)

    size_scores.name = "size_score"
    quality_scores.name = "quality_score"

    momentum_z.to_csv("data/processed/momentum_scores.csv")
    momentum_z = pd.read_csv(
        "data/processed/momentum_scores.csv",
        index_col="Date",
        parse_dates=True
    )

    value_z.to_csv("data/processed/value_scores.csv")
    value_z = pd.read_csv(
        "data/processed/value_scores.csv",
        index_col="Date",
        parse_dates=True
    )

    size_scores.to_frame().rename_axis("ticker").round(5)\
        .to_csv("data/processed/size_scores.csv")
    size_scores = pd.read_csv(
        "data/processed/size_scores.csv",
        index_col=0
    ).iloc[:, 0]
    
    quality_scores.to_frame().rename_axis("ticker").round(5)\
        .to_csv("data/processed/quality_scores.csv")
    quality_scores = pd.read_csv(
        "data/processed/quality_scores.csv",
        index_col=0
    ).iloc[:, 0]

    composite_scores = compute_composite_scores(
        momentum_z,
        value_z,
        size_scores,
        quality_scores
    )
    composite_scores.to_csv("data/processed/composite_scores.csv")

    monthly_prices = pd.read_csv(
        "data/processed/monthly_prices.csv",
        index_col=0,
        parse_dates=True
    )
    composite_scores = pd.read_csv(
        "data/processed/composite_scores.csv",
        index_col="Date",
        parse_dates=True
    )

    common_dates = composite_scores.index.intersection(monthly_prices.index)
    composite_scores = composite_scores.loc[common_dates]
    monthly_prices = monthly_prices.loc[common_dates]

    portfolio_returns, portfolio_weights = construct_equal_weight_portfolio_with_costs(
        composite_scores,
        monthly_prices,
        top_pct=0.2,
        transaction_cost=0.001
    )
    portfolio_returns.to_csv("data/processed/portfolio_returns.csv")
    portfolio_weights.to_csv("data/processed/portfolio_weights.csv")
    portfolio_returns = pd.read_csv(
        "data/processed/portfolio_returns.csv",
        index_col=0,
        parse_dates=True
    )

    benchmark_returns = construct_equal_weight_benchmark(monthly_prices)
    benchmark_returns.to_csv("data/processed/benchmark_returns.csv")
    benchmark_cum_returns = (1 + benchmark_returns["benchmark_return"]).cumprod()
    benchmark_cum_returns.to_csv("data/processed/benchmark_cumulative_returns.csv")

    strategy_returns = portfolio_returns["net_return"]
    benchmark_returns = benchmark_returns["benchmark_return"]
    strategy_metrics = portfolio_vs_benchmark(strategy_returns)
    benchmark_metrics = portfolio_vs_benchmark(benchmark_returns)
    performance_table = pd.DataFrame([strategy_metrics, benchmark_metrics], index=["Strategy", "Benchmark"])
    performance_table.to_csv("data/processed/performance_comparison.csv")

    spy_returns = get_spy_returns(
        start_date=portfolio_returns.index.min(),
        end_date=portfolio_returns.index.max()
    )    
    aligned = pd.concat([portfolio_returns, spy_returns], axis=1).dropna()
    net_returns = portfolio_returns.loc[aligned.index, "net_return"]
    spy_returns = aligned["SPY"]

    performance_summary = pd.DataFrame({
        "Annualized Return": [
            annualized_return(net_returns),
            annualized_return(spy_returns)
        ],
        "Annualized Volatility": [
            annualized_volatility(net_returns),
            annualized_volatility(spy_returns)
        ],
        "Sharpe Ratio": [
            sharpe_ratio(net_returns),
            sharpe_ratio(spy_returns)
        ],
        "Max Drawdown": [
            max_drawdown(net_returns),
            max_drawdown(spy_returns)
        ]
    }, index=["Multi-Factor Portfolio", "SPY"])
    performance_summary.to_csv("data/processed/performance_summary.csv")

    cumulative_returns = (1 + aligned).cumprod()
    cumulative_returns.to_csv("data/processed/cumulative_returns.csv")

    portfolio_returns = pd.read_csv(
        "data/processed/portfolio_returns.csv",
        index_col=0,
        parse_dates=True
    )["net_return"]
    monthly_prices = pd.read_csv(
        "data/processed/monthly_prices.csv",
        index_col=0,
        parse_dates=True
    )

    momentum = pd.read_csv("data/processed/momentum_scores.csv", index_col=0, parse_dates=True)
    value = pd.read_csv("data/processed/value_scores.csv", index_col=0, parse_dates=True)
    size = pd.read_csv("data/processed/size_scores.csv", index_col="ticker")["size_score"]
    quality = pd.read_csv("data/processed/quality_scores.csv", index_col="ticker")["quality_score"]

    dates = monthly_prices.index
    size_scores_ts = expand_static_factor(size, dates)
    quality_scores_ts = expand_static_factor(quality, dates)

    factor_returns = {
        "Momentum": compute_factor_returns(momentum, monthly_prices),
        "Value": compute_factor_returns(value, monthly_prices),
        "Size": compute_factor_returns(size_scores_ts, monthly_prices),
        "Quality": compute_factor_returns(quality_scores_ts, monthly_prices),
    }
    factor_returns_df = pd.concat( factor_returns.values(), axis=1)
    factor_returns_df.columns = factor_returns.keys()
    factor_corr = factor_returns_df.corr()
    factor_corr.to_csv("data/processed/factor_correlation.csv")

    attribution_table, attribution_model = factor_attribution(strategy_returns, factor_returns_df)
    attribution_table.to_csv("data/processed/factor_attribution.csv")

    betas = attribution_table["Coefficient"]
    alpha_table = alpha_decomposition( strategy_returns, factor_returns_df, betas)
    alpha_table.to_csv("data/processed/alpha_decomposition.csv")

if __name__ == "__main__":
    main()
