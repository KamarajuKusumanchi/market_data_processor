#! /usr/bin/env python3

# Sample usage
# $ $market_data_processor/src/nasdaq/get_marketcap_change.py > ~/x/market_cap_change.csv
# $ csvcut -c symbol,marketCap,marketcap_change,pctchange ~/x/market_cap_change.csv | column -t -s, -R 2,3,4 | head
# symbol          marketCap  marketcap_change  pctchange
# GOOGL             1260.85           -117.70      -8.54
# GOOG              1267.69           -115.98      -8.38
# AAPL              2636.32            -44.91      -1.68
# AMZN              1005.78            -33.38      -3.21
# META               474.89            -21.91      -4.41
# ASML               267.14             -6.48      -2.37
# CVX                330.61             -6.02      -1.79
# FTNT                47.64              5.24      12.37
# TSLA               627.86              5.14       0.82

import sys
import numpy as np
import pandas as pd
import argparse

import project_root
from src.nasdaq.get_nasdaq_data import get_nasdaq_df


def create_parser():
    parser = argparse.ArgumentParser("Get changes in the market cap values")
    return parser


def get_marketcap_change(df: pd.DataFrame):
    # remove rows where either percent change or market cap are missing.
    mask = df["marketCap"].isna() | df["pctchange"].isna()
    df = df[~mask].copy()
    change = df["pctchange"] / 100
    marketcap_change = (df["marketCap"] * change) / (1 + change)
    col_name = "marketcap_change"
    # insert this after the marketCap column
    df.insert(df.columns.get_loc("marketCap") + 1, col_name, marketcap_change)
    # Sort by the absolute value of market cap change
    df = df.iloc[(-df[col_name].abs()).argsort()].reset_index(drop=True)
    # Put important columns at the beginning
    high_priority_cols = ["symbol", "marketCap", col_name, "pctchange"]
    least_priority_cols = ["name"]
    cols_accounted = high_priority_cols + least_priority_cols
    cols_unaccounted = [col for col in df.columns if col not in cols_accounted]
    df = df[high_priority_cols + cols_unaccounted + least_priority_cols]
    return df


def run_code():
    parser = create_parser()
    args = parser.parse_args()
    df = get_nasdaq_df()
    in_billions = True
    if in_billions:
        df["marketCap"] /= 1e9
    df = get_marketcap_change(df)
    pd.set_option("display.max_columns", None, "display.max_rows", None)
    df.index = np.arange(len(df)) + 1
    # df.to_csv(sys.stdout, index=False, lineterminator='\n')
    # df.round({"marketCap": 2, "marketcap_change": 2, "pctchange": 2}).to_csv(
    #     sys.stdout, index=False, lineterminator="\n"
    # )
    # Using https://stackoverflow.com/a/62546734 to format columns
    formats = {
        "marketCap": "{:.2f}",
        "marketcap_change": "{:.2f}",
        "pctchange": "{:.2f}",
    }
    for col, f in formats.items():
        df[col] = df[col].apply(lambda x: f.format(x))
    df.to_csv(sys.stdout, index=False, lineterminator="\n")


if __name__ == "__main__":
    run_code()
