# Model Assumptions — Multi-Factor Equity Portfolio Strategy

This document outlines the assumptions used in constructing and evaluating
the multi-factor equity portfolio strategy.

---

## 1. Universe & Data Assumptions

- Equity universe consists of S&P 500 constituents
- Survivorship bias may exist depending on data availability
- Prices and fundamentals are assumed to be correctly adjusted
- Missing data is handled through cross-sectional filtering

---

## 2. Factor Construction Assumptions

- Factor definitions are based on established academic literature
- Signals are constructed using historical data only (no look-ahead bias)
- Factors are normalized cross-sectionally
- Equal weighting is used when combining factor scores unless specified

---

## 3. Portfolio Construction Assumptions

- Portfolio is long-only
- Positions are rebalanced at fixed intervals
- Equal-weighted or score-weighted allocations are used
- No leverage is applied

---

## 4. Transaction Cost Assumptions

- Transaction costs are modeled as linear proportional costs
- Market impact and slippage are not explicitly modeled
- Costs are applied during rebalancing events only

---

## 5. Risk & Performance Assumptions

- Returns are evaluated using historical realized performance
- Risk metrics assume stable return distributions within each evaluation window
- Benchmark comparisons are relative to the S&P 500 index

---

## 6. Attribution Assumptions

- Regression-based attribution assumes linear factor relationships
- Alpha represents unexplained excess return after factor exposure
- Factor correlations may change across market regimes

---

## 7. Model Limitations

- Factor performance may degrade over time
- Structural market changes are not modeled
- Results are sensitive to rebalance frequency and signal definitions
- No dynamic factor timing is implemented

---

## 8. Intended Scope

This framework is intended for:
- Educational purposes
- Quantitative research
- Demonstration of systematic equity strategy design

It is not intended for live trading or capital allocation decisions.
