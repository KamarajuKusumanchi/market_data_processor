#! /usr/bin/env python3
# Get market cap
import argparse

import requests
import pandas as pd
import pprint
import os


def create_parser():
    parser = argparse.ArgumentParser(description="Get market cap")
    parser.add_argument(
        "--limit", action="store", dest="limit", help="Limit to N entries", default=None
    )
    return parser


def get_nasdaq_data():
    # I found this url as follows:
    # Go to https://www.nasdaq.com/market-activity/stocks/screener in chrome
    # -> F12 -> Network
    # -> click on the "Download CSV" button and watch the requests at the
    # bottom which shows that it is getting data from
    # https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=25&offset=0&download=true
    #
    # Ref:- https://stackoverflow.com/questions/70283880/cant-find-hyper-link-for-this-csv-file-on-website
    url = "https://api.nasdaq.com/api/screener/stocks?download=true"
    # To get around the connection timeour errors,
    # https://stackoverflow.com/questions/61943209/accessing-nasdaq-historical-data-with-python-requests-results-in-connection-time
    # suggests to use the following headers.
    headers = {
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "User-Agent": "Java-http-client/",
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    return data


def dump_nasdaq_data(data):
    """
    :param data: dictionary
    :return:
    """
    # Ref:- https://stackoverflow.com/questions/4028904/what-is-a-cross-platform-way-to-get-the-home-directory
    home = os.path.expanduser("~")
    path = os.path.join(home, "x", "nasdaq_data.py")
    print("writing nasdaq data to", path)
    # Note: pprint is discussed in https://automatetheboringstuff.com/2e/chapter9/
    # -> Saving Variables with the pprint.pformat() Function
    fileObj = open(path, "w")
    fileObj.write("nasdaq_data = " + pprint.pformat(data) + "\n")
    fileObj.close()


def convert_nasdaq_data_to_df(data):
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


def get_market_cap(nasdaq_df, limit):
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
    # dump_nasdaq_data(nasdaq_data)
    nasdaq_df = convert_nasdaq_data_to_df(nasdaq_data)
    market_cap = get_market_cap(nasdaq_df, limit)
    pd.set_option("display.max_columns", None, "display.max_rows", None)
    # print(market_cap.to_csv(index=False))
    print(market_cap)


if __name__ == "__main__":
    run_code()
