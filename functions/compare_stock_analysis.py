import pandas as pd
import os
from scipy.stats import linregress
from tabulate import tabulate  # For beautified table output
import matplotlib.pyplot as plt

# Calculate Moving Average
def calculate_moving_average(data, column="4. close", window=50):
    return data[column].rolling(window=window).mean()

# Calculate Sharpe Ratio
def calculate_sharpe_ratio(data, column="4. close", risk_free_rate=0.02):
    returns = data[column].pct_change()
    excess_returns = returns.mean() - (risk_free_rate / 252)
    return excess_returns / returns.std()

# Calculate Volatility
def calculate_volatility(data, column="4. close"):
    return data[column].pct_change().std()

# Calculate CAGR
def calculate_cagr(data, column="4. close"):
    start_price = data[column].iloc[0]
    end_price = data[column].iloc[-1]
    years = len(data) / 252
    return (end_price / start_price) ** (1 / years) - 1

# Calculate RSI
def calculate_rsi(data, column="4. close", window=14):
    delta = data[column].diff()
    gain = delta.where(delta > 0, 0).rolling(window=window).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

# Calculate Beta
def calculate_beta_simple(stock_data, benchmark_data, column="4. close"):
    stock_returns = stock_data[column].pct_change()
    benchmark_returns = benchmark_data.pct_change()
    beta, _, _, _, _ = linregress(benchmark_returns[1:], stock_returns[1:])
    return beta

# Calculate Max Drawdown
def calculate_max_drawdown(data, column="4. close"):
    cumulative_max = data[column].cummax()
    drawdown = (data[column] - cumulative_max) / cumulative_max
    return drawdown.min()

# Compare Stocks
def compare_stock_analysis(stock1, stock2, stock_data, benchmark_data):
    metrics = ["Moving Average", "Sharpe Ratio", "Volatility", "CAGR", "RSI", "Beta", "Max Drawdown"]
    results = {stock1: {}, stock2: {}}
    points = {stock1: 0, stock2: 0}

    data1 = stock_data[stock1]
    data2 = stock_data[stock2]

    benchmark_col1 = f"close ({stock1.lower()})"
    benchmark_col2 = f"close ({stock2.lower()})"

    benchmark1 = benchmark_data[benchmark_col1]
    benchmark2 = benchmark_data[benchmark_col2]

    for metric in metrics:
        if metric == "Moving Average":
            results[stock1][metric] = round(calculate_moving_average(data1).iloc[-1], 3)
            results[stock2][metric] = round(calculate_moving_average(data2).iloc[-1], 3)
        elif metric == "Sharpe Ratio":
            results[stock1][metric] = round(calculate_sharpe_ratio(data1), 3)
            results[stock2][metric] = round(calculate_sharpe_ratio(data2), 3)
        elif metric == "Volatility":
            results[stock1][metric] = round(calculate_volatility(data1), 3)
            results[stock2][metric] = round(calculate_volatility(data2), 3)
        elif metric == "CAGR":
            results[stock1][metric] = round(calculate_cagr(data1), 3)
            results[stock2][metric] = round(calculate_cagr(data2), 3)
        elif metric == "RSI":
            results[stock1][metric] = round(calculate_rsi(data1).iloc[-1], 3)
            results[stock2][metric] = round(calculate_rsi(data2).iloc[-1], 3)
        elif metric == "Beta":
            results[stock1][metric] = round(calculate_beta_simple(data1, benchmark1), 3)
            results[stock2][metric] = round(calculate_beta_simple(data2, benchmark2), 3)
        elif metric == "Max Drawdown":
            results[stock1][metric] = round(calculate_max_drawdown(data1), 3)
            results[stock2][metric] = round(calculate_max_drawdown(data2), 3)

    for metric in metrics:
        if metric in ["Volatility", "Beta", "Max Drawdown"]:  # Lower is better
            winner = min(results, key=lambda x: results[x][metric])
        else:  # Higher is better
            winner = max(results, key=lambda x: results[x][metric])
        points[winner] += 1

    comparison_df = pd.DataFrame(results).T
    for metric in metrics:
        if metric in ["Volatility", "Beta", "Max Drawdown"]:
            best_stock = comparison_df[metric].idxmin()
        else:
            best_stock = comparison_df[metric].idxmax()
        comparison_df.loc[best_stock, metric] = f"{comparison_df.loc[best_stock, metric]} ★"

    comparison_df["Points"] = [points[stock1], points[stock2]]
    return comparison_df

# Plot Comparison Results
def plot_comparison_results(results):
    results_numeric = results.drop(columns=["Points"], errors="ignore").replace(r" ★", "", regex=True)
    results_numeric = results_numeric.apply(pd.to_numeric, errors="coerce")
    results_numeric.T.plot(kind="bar", figsize=(10, 6), colormap="viridis")
    plt.title("Stock Comparison Metrics")
    plt.ylabel("Values")
    plt.xticks(rotation=45)
    plt.legend(title="Stocks")
    plt.grid(axis="y")
    plt.tight_layout()
    plt.show()

# Main Execution Block
if __name__ == "__main__":
    # Load all stocks
    stock_data = {
        "NVDA": pd.read_csv("../data/nvda_daily.csv"),
        "GOOG": pd.read_csv("../data/goog_daily.csv"),
        "AMZN": pd.read_csv("../data/amzn_daily.csv"),
        "META": pd.read_csv("../data/meta_daily.csv"),
        "TSLA": pd.read_csv("../data/tsla_daily.csv"),
        "ORCL": pd.read_csv("../data/orcl_daily.csv"),
    }
    combined_data = pd.read_csv("../data/combined_stocks.csv")

    # User input for stock comparison
    print("Available stocks:", list(stock_data.keys()))
    stock1 = input("Enter the first stock ticker: ").upper()
    stock2 = input("Enter the second stock ticker: ").upper()

    if stock1 not in stock_data or stock2 not in stock_data:
        print("Invalid stock tickers. Please choose from the available stocks.")
    else:
        # Compare stocks
        results = compare_stock_analysis(stock1, stock2, stock_data, combined_data)

        # Beautified table output
        print("\nComparison Results:")
        print(tabulate(results, headers="keys", tablefmt="grid"))
