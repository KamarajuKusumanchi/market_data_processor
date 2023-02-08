#! /usr/bin/env python3

# Sample usage
# $ $market_data_processor/src/nasdaq/get_marketcap_change.py > ~/x/market_cap_change.csv
# $ csvcut -c symbol,marketCap,marketcap_change,pctchange ~/x/market_cap_change.csv | column -t -s, -R 2,3,4 | head
# symbol          marketCap  marketcap_change  pctchange
# MSFT              1991.66             80.31        4.2
# GOOGL             1378.55              60.7       4.61
# GOOG              1383.67             58.53       4.42
# AAPL              2681.22             50.61       1.92
# NVDA               545.46             26.67       5.14
# META                496.8             14.41       2.99
# TSM                490.34             14.11       2.96
# XOM                 469.1             13.02       2.86
# BRK/A              698.01             11.11       1.62

import sys
import numpy as np
import pandas as pd

import project_root
from src.nasdaq.get_nasdaq_data import get_nasdaq_df


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
    important_cols = ['symbol', 'marketCap', col_name, 'pctchange']
    unimportant_cols = [col for col in df.columns if col not in important_cols]
    df = df[important_cols + unimportant_cols]
    return df


def run_code():
    df = get_nasdaq_df()
    in_billions = True
    if in_billions:
        df["marketCap"] /= 1e9
    df = get_marketcap_change(df)
    pd.set_option("display.max_columns", None, "display.max_rows", None)
    df.index = np.arange(len(df)) + 1
    # df.to_csv(sys.stdout, index=False, lineterminator='\n')
    df.round({"marketCap": 2, "marketcap_change": 2, "pctchange": 2}).to_csv(
        sys.stdout, index=False, lineterminator="\n"
    )


if __name__ == "__main__":
    run_code()
