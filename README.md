# Multi-Factor Equity Portfolio Strategy (S&P 500)

An end-to-end **systematic equity portfolio construction framework** based on classical equity factor models.

The project mirrors the **quant research workflow** used by systematic equity and factor investing teams.

---

## Project Objective

To research, implement, and evaluate a multi-factor equity strategy by:
- Constructing interpretable factor signals
- Combining signals into systematic portfolios
- Incorporating rebalancing and transaction costs
- Measuring performance, risk, and factor-driven alpha

---

## Factor Signals Implemented

- Momentum
- Value
- Size
- Quality

Each factor is independently constructed, normalized, and analyzed
before portfolio aggregation.

---

## Portfolio Construction Framework

- Universe: S&P 500 equities
- Cross-sectional factor ranking
- Composite factor score construction
- Periodic portfolio rebalancing
- Long-only factor-tilted portfolio formation
- Transaction-cost–adjusted return computation

---

## Research & Performance Analysis

- Cumulative and annualized returns
- Volatility and drawdown analysis
- Benchmark comparison against S&P 500
- Factor correlation analysis
- Regression-based attribution and alpha decomposition

---

## Risk & Attribution Insights

- Factor exposure decomposition
- Return attribution by factor contribution
- Analysis of factor diversification benefits
- Stability of factor performance across market regimes

---

## Project Structure
multi_factor_portfolio/
├── analytics/
│ └── alpha_decomposition.py
│ └── factor_attribution.py
│ └── performance_metrics.py
├── data/
│ ├── download_prices.py
│ ├── get_sp500_tickers.py
│ ├── market_cap.py
│ ├── quality_data.py
│ ├── processed/
│ │ ├── alpha_decomposition.csv
│ │ ├── benchmark_cumulative_returns.csv
│ │ ├── benchmark_returns.csv
│ │ ├── composite_scores.csv
│ │ ├── cumulative_returns.csv
│ │ ├── eligible_universe.csv
│ │ ├── factor_attribution.csv
│ │ ├── factor_correlation.csv
│ │ ├── momentum_scores.csv
│ │ ├── monthly_prices.csv
│ │ ├── performance_comparison.csv
│ │ ├── portfolio_returns.csv
│ │ ├── portfolio_weights.csv
│ │ ├── quality_scores.csv
│ │ ├── size_scores.csv
│ │ └── value_scores.csv
│ └── universe/
│ │ └── sp500_constituents.csv
├── factors/
│ ├── composite_time_series.py
│ ├── momentum.py
│ ├── quality.py
│ ├── size.py
│ └── value.py
├── performance/
│ ├── benchmark.py
│ ├── metrics.py
│ └── plots.py
├── portfolio/
│ ├── benchmark.py
│ └── portfolio_construction.py
├── main.py
├── visualization.py
├── README.md
└── MODEL_ASSUMPTIONS.md

---

## Tech Stack

- Python
- Pandas
- NumPy
- Statsmodels
- Financial data APIs (e.g., yfinance)

---

## Intended Use

- Systematic equity research
- Factor-based portfolio construction
- Quantitative investment analysis

---

## Disclaimer

This project is for educational and research purposes only and does not constitute investment advice.
