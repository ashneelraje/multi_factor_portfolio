import pandas as pd
import numpy as np

def compute_quality_scores(roe_series, winsorize_level=0.05):
    
    roe = roe_series.dropna()

    lower = roe.quantile(winsorize_level)
    upper = roe.quantile(1 - winsorize_level)
    roe = roe.clip(lower, upper)

    roe_z = (roe - roe.mean()) / roe.std()

    roe_z.name = "quality_score"

    return roe_z
