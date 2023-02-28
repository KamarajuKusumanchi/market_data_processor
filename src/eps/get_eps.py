#! /usr/bin/env python3

import argparse
import pandas as pd
import sys

import project_root
from src.utils.DataFrameUtils import to_fwf


def run_code():
    parser = create_parser()
    args = parser.parse_args()
    ticker = args.ticker.upper()
    eps = get_eps(ticker)
    eps.to_fwf(sys.stdout, index=False)


def create_parser():
    parser = argparse.ArgumentParser(description="Get eps of a company")
    parser.add_argument("ticker", action="store", help="ticker")
    parser.add_argument(
        "--debug",
        action="store_true",
        default=False,
        dest="debug",
        help="show debug output",
    )
    return parser


def get_eps(ticker):
    url = f"https://www.alphaquery.com/stock/{ticker}/earnings-history"
    dfs = pd.read_html(url)
    df = dfs[0]
    return df


if __name__ == "__main__":
    run_code()
