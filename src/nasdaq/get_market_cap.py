#! /usr/bin/env python3
# Get market cap

# tags: download market cap of all sp500 companies

import argparse
import numpy as np
import pandas as pd

import project_root
from src.nasdaq.get_nasdaq_data import get_nasdaq_data, convert_nasdaq_data_to_df


def create_parser():
    parser = argparse.ArgumentParser(description="Get market cap")
    parser.add_argument(
        "--limit", action="store", dest="limit", help="Limit to N entries", default=None
    )
    return parser


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
