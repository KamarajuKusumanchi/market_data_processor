#! /usr/bin/env python3

# Sample usage
# $ $market_data_processor/src/nasdaq/get_mktcap_change.py > ~/x/nasdaq.csv
# $ csvcut -c symbol,marketCap,mktcap_change,pctchange ~/x/nasdaq.csv | column -t -s, -R 2,3,4 | head
# symbol          marketCap  mktcap_change  pctchange
# AAPL              2703.38          88.56       3.39
# AMZN              1096.71         -52.36      -4.56
# TSLA                622.0          26.29       4.41
# GOOG              1386.45         -21.74      -1.54
# GEN                225.42         -20.22      -8.23
# MSFT              1950.98         -18.65      -0.95
# META               436.68          10.94       2.57
# GOOGL             1383.74         -10.74      -0.77
# NVO                307.59          10.04       3.37

import sys
import numpy as np
import pandas as pd

import project_root
from src.nasdaq.get_nasdaq_data import get_nasdaq_df


def get_mktcap_change(df: pd.DataFrame):
    # remove rows where either percent change or market cap are missing.
    mask = df["marketCap"].isna() | df["pctchange"].isna()
    df = df[~mask].copy()
    change = df["pctchange"] / 100
    mktcap_change = (df["marketCap"] * change) / (1 + change)
    col_name = "mktcap_change"
    # insert this after the marketCap column
    df.insert(df.columns.get_loc("marketCap") + 1, col_name, mktcap_change)
    # Sort by the absolute value of market cap change
    df = df.iloc[(-df[col_name].abs()).argsort()].reset_index(drop=True)
    return df


def run_code():
    df = get_nasdaq_df()
    in_billions = True
    if in_billions:
        df["marketCap"] /= 1e9
    df = get_mktcap_change(df)
    pd.set_option("display.max_columns", None, "display.max_rows", None)
    df.index = np.arange(len(df)) + 1
    # df.to_csv(sys.stdout, index=False, lineterminator='\n')
    df.round({"marketCap": 2, "mktcap_change": 2, "pctchange": 2}).to_csv(
        sys.stdout, index=False, lineterminator="\n"
    )


if __name__ == "__main__":
    run_code()
