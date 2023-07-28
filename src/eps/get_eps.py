#! /usr/bin/env python3
# Get eps history

# Sample run
#  % python src/eps/get_eps.py COST | head
#  Announcement Date    Fiscal Quarter End    Estimated EPS    Actual EPS
#  2022-12-08           2022-11-30            $3.14            $3.10
#  2022-09-22           2022-08-31            $4.12            $4.20
#  2022-05-26           2022-05-31            $3.00            $3.17
#  2022-03-03           2022-02-28            $2.69            $2.92
#  2021-12-09           2021-11-30            $2.59            $2.97
#  2021-09-23           2021-08-31            $3.55            $3.90
#  2021-05-27           2021-05-31            $2.29            $2.75
#  2021-03-04           2021-02-28            $2.42            $2.14
#  2020-12-10           2020-11-30            $2.04            $2.29

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
    # The initial column names are something like
    # ['Announcement Date', 'Fiscal Quarter End', 'Estimated EPS', 'Actual EPS']
    # The spaces in the column names will cause problems when the data is
    # loaded into excel if we were to dump the dataframe itself with space
    # delimiters.
    df.columns = df.columns.str.lower().str.replace(" ", "_")
    # Estimated EPS and Actual EPS are something like $1.28 .
    # Remove the leading '$' and convert the rest into a number.
    df["estimated_eps"] = (
        df["estimated_eps"]
        .str.replace(r"^\$", "", regex=True)
        .apply(pd.to_numeric, errors="coerce")
    )
    df["actual_eps"] = (
        df["actual_eps"]
        .str.replace(r"^\$", "", regex=True)
        .apply(pd.to_numeric, errors="coerce")
    )
    return df


if __name__ == "__main__":
    run_code()
