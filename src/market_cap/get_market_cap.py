#! /usr/bin/env python3
# Get market cap
import argparse
import numpy as np
import pandas as pd

import sys_path
from src.market_cap.get_nasdaq_data import get_nasdaq_data


def create_parser():
    parser = argparse.ArgumentParser(description="Get market cap")
    parser.add_argument(
        "--limit", action="store", dest="limit", help="Limit to N entries", default=None
    )
    return parser


def convert_nasdaq_data_to_df(data: dict) -> pd.DataFrame:
    df = pd.DataFrame(data["data"]["rows"])
    # The marketCap column contains empty strings. So, if I do
    #   df['marketCap'] = df['marketCap'].astype('float')
    # it gives
    #   ValueError: could not convert string to float: ''
    # As a workaround, I am using pandas.to_numeric with errors='coerce'
    # which will convert any value error to NaN
    # Ref:- https://pandas.pydata.org/docs/reference/api/pandas.to_numeric.html
    df["marketCap"] = pd.to_numeric(df["marketCap"], errors="coerce")
    return df


def get_market_cap(nasdaq_df: pd.DataFrame, limit: int) -> pd.DataFrame:
    """
    :param nasdaq_df: dataFrame
    :return: dataFrame
    """
    market_cap = nasdaq_df[["symbol", "marketCap"]]
    market_cap = market_cap.sort_values("marketCap", ascending=False, ignore_index=True)
    if limit:
        market_cap = market_cap.loc[: limit - 1, :]
    market_cap["pct_weight"] = (
        market_cap["marketCap"] / market_cap["marketCap"].sum()
    ) * 100
    return market_cap


def run_code():
    parser = create_parser()
    args = parser.parse_args()
    limit = int(args.limit) if args.limit else None
    nasdaq_data = get_nasdaq_data()
    nasdaq_df = convert_nasdaq_data_to_df(nasdaq_data)
    market_cap = get_market_cap(nasdaq_df, limit)
    pd.set_option("display.max_columns", None, "display.max_rows", None)
    market_cap.index = np.arange(len(market_cap)) + 1
    # print(market_cap.to_csv(index=False))
    print(market_cap)


if __name__ == "__main__":
    run_code()
