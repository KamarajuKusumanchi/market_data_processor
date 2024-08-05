# Install necessary libraries
import yfinance as yf
import pandas as pd
import numpy as np

from sp500_tickers import get_sp500_tickers


def calculate_sharpe_ratio(tickers, start_date, end_date, risk_free_rate=0.01):
    # Download historical stock prices
    data = yf.download(tickers, start=start_date, end=end_date)["Adj Close"]

    # Calculate daily returns
    daily_returns = data.pct_change().dropna()

    # Calculate the mean and standard deviation of daily returns
    mean_daily_returns = daily_returns.mean()
    std_daily_returns = daily_returns.std()

    # Calculate the annualized Sharpe ratio
    sharpe_ratios = (
        (mean_daily_returns - risk_free_rate / 252) / std_daily_returns * np.sqrt(252)
    )

    return sharpe_ratios


def run_sharpe_ratio():
    # Define parameters
    tickers = ["AAPL", "MSFT", "GOOGL", "AJG", "MCK", "SPY"]  # Example tickers
    start_date = "2021-08-01"
    end_date = "2024-07-31"
    risk_free_rate = 0.05  # Example risk-free rate (1%)

    # Calculate Sharpe ratios
    sharpe_ratios = calculate_sharpe_ratio(
        tickers, start_date, end_date, risk_free_rate
    )
    print(sharpe_ratios)


def sharpe_ratio_of_sp500_tickers():
    tickers = ["AAPL", "MSFT", "GOOGL", "AJG", "MCK", "SPY", "GL"]
    # There is something wrong with the calculation of sharpe ratio.
    # I am getting different values when using individual tickers like above
    # and when using all sp500 tickers as below. Probably something to do
    # with treatment of NaNs. Debug this later.
    # tickers = get_sp500_tickers()
    start_date = "2021-08-01"
    end_date = "2024-07-31"
    risk_free_rate = 0.05  # risk free rate is 5%
    sharpe_ratios = calculate_sharpe_ratio(
        tickers, start_date, end_date, risk_free_rate
    )
    sharpe_ratios = sharpe_ratios.sort_values()
    return sharpe_ratios


if __name__ == "__main__":
    # run_sharpe_ratio()
    sharpe_ratios = sharpe_ratio_of_sp500_tickers()
    print(sharpe_ratios)
