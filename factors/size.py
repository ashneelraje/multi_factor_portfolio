import pandas as pd

def compute_size_scores(market_cap):
    
    market_cap = market_cap.dropna()
    size_rank = market_cap.rank(pct=True, ascending=True)
    size_scores = 1 - size_rank
    size_scores.name = "size_score"

    return size_scores