import pandas as pd

def alpha_decomposition(
    strategy_returns: pd.Series,
    factor_returns: pd.DataFrame,
    betas: pd.Series
):

    aligned = pd.concat(
        [strategy_returns, factor_returns],
        axis=1,
        join="inner"
    ).dropna()

    betas = betas.drop("const")

    explained = (aligned[factor_returns.columns] * betas).sum(axis=1)
    alpha = aligned[strategy_returns.name] - explained

    decomposition = pd.DataFrame({
        "strategy_return": aligned[strategy_returns.name],
        "explained_return": explained,
        "alpha_return": alpha
    })

    return decomposition
