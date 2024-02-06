#! /usr/bin/env python3
# Compute the P/E of S&P500 index
import pandas as pd
from finvizfinance.screener.overview import Overview
from datetime import date

from pandas import DataFrame

from key_stats import print_full


def compute_pe():
    foverview = Overview()
    # Use this to test
    # filters_dict = {'Index': 'S&P 500', 'Sector': 'Basic Materials'}
    # Use this for full run
    filters_dict = {"Index": "S&P 500"}
    foverview.set_filter(filters_dict=filters_dict)
    df = foverview.screener_view()
    # print_full(df.head())

    # screener_view() gives ['Ticker', 'Company', 'Sector', 'Industry',
    # 'Country', 'Market Cap', 'P/E', 'Price', 'Change', 'Volume'] columns
    total_market_cap = df["Market Cap"].sum()
    df["Earnings"] = df["Market Cap"] / df["P/E"]
    total_earnings = df["Earnings"].sum()
    pe_ratio = total_market_cap / total_earnings
    earnings_yield = (total_earnings / total_market_cap) * 100

    cob = date.today().isoformat()
    pe: DataFrame = pd.DataFrame(
        [[cob, "sp500", total_market_cap, total_earnings, pe_ratio, earnings_yield]],
        columns=["cob", "index", "market_cap", "earnings", "pe", "earnings_yield"],
    )
    return pe


def main():
    df = compute_pe()
    print_full(df)


if __name__ == "__main__":
    main()
