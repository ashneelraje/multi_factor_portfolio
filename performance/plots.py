import pandas as pd
import matplotlib.pyplot as plt

def plot_cumulative_returns(file_path):
    cumulative_returns = pd.read_csv(
        file_path,
        index_col=0,
        parse_dates=True
    )

    plt.figure(figsize=(12, 6))
    plt.plot(cumulative_returns.index, cumulative_returns.iloc[:, 1], label="Multi-Factor Portfolio")
    plt.plot(cumulative_returns.index, cumulative_returns.iloc[:, 4], label="SPY")

    plt.title("Cumulative Returns: Multi-Factor Portfolio vs SPY")
    plt.xlabel("Date")
    plt.ylabel("Growth of $1")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
