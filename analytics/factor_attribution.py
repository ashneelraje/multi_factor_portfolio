import pandas as pd
import statsmodels.api as sm

def factor_attribution(
    strategy_returns: pd.Series,
    factor_returns: pd.DataFrame
):

    aligned = pd.concat(
        [strategy_returns, factor_returns],
        axis=1,
        join="inner"
    ).dropna()

    y = aligned.iloc[:, 0]  # strategy returns
    X = aligned.iloc[:, 1:]  # factor returns

    X = sm.add_constant(X)

    model = sm.OLS(y, X).fit()

    results = pd.DataFrame({
        "Coefficient": model.params,
        "t_stat": model.tvalues,
        "p_value": model.pvalues
    })

    return results, model
