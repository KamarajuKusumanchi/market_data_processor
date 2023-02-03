#! /usr/bin/env python3

import sys
import numpy as np
import pandas as pd

import project_root
from src.nasdaq.get_nasdaq_data import get_nasdaq_df

def get_mktcap_change(df: pd.DataFrame):
    # remove rows where either percent change or market cap are missing.
    mask = (df['marketCap'].isna() | df['pctchange'].isna())
    df = df[~mask].copy()
    change = df['pctchange'] / 100
    mktcap_change = (df['marketCap'] * change) / (1 + change)
    col_name = "mktcap_change"
    # insert this after the marketCap column
    df.insert(df.columns.get_loc('marketCap')+1, col_name, mktcap_change)
    # Sort by the absolute value of market cap change
    df = df.iloc[(-df[col_name].abs()).argsort()].reset_index(drop=True)
    return df


def run_code():
    df = get_nasdaq_df()
    in_billions = True
    if in_billions:
        df['marketCap'] /= 1e9
    df = get_mktcap_change(df)
    pd.set_option("display.max_columns", None, "display.max_rows", None)
    df.index = np.arange(len(df)) + 1
    df.to_csv(sys.stdout, index=False, lineterminator='\n')


if __name__ == "__main__":
    run_code()