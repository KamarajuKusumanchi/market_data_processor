#! /usr/bin/env python3

# Get nasdaq data.
# Sample run
# get_nasdaq_data.py | body grep -i costco | column -t -s ,
# symbol  name                                       lastsale  netchange  pctchange  volume   marketCap       country        ipoyear  industry                            sector                  url
# COST    Costco Wholesale Corporation Common Stock  $503.29   4.99       1.001%     2032821  223324386528.0  United States           Department/Specialty Retail Stores  Consumer Discretionary  /market-activity/stocks/cost

# tags: "https://www.nasdaq.com/market-activity/stocks/screener"

import argparse
import os
import pprint
import sys

import pandas as pd
import requests
from typing import Dict, Any


def create_parser():
    parser = argparse.ArgumentParser(description="Get nasdaq data")
    parser.add_argument(
        "-o",
        "--output",
        dest="output_file",
        type=argparse.FileType("w"),
        default=sys.stdout,
        help="output file",
    )
    return parser


def get_nasdaq_data() -> Dict[str, Any]:
    # I found this url as follows:
    # Go to https://www.nasdaq.com/market-activity/stocks/screener in chrome
    # -> F12 -> Network
    # -> click on the "Download CSV" button and watch the requests at the
    # bottom which shows that it is getting data from
    # https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=25&offset=0&download=true
    #
    # Ref:- https://stackoverflow.com/questions/70283880/cant-find-hyper-link-for-this-csv-file-on-website
    url = "https://api.nasdaq.com/api/screener/stocks?download=true"
    # To get around the connection timeout errors,
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


def dump_raw_nasdaq_data(data: dict, path: str):
    """
    :param data: dictionary
    :return:
    """
    if path is not sys.stdout:
        print("writing nasdaq data to", path)
    # Note: pprint is discussed in https://automatetheboringstuff.com/2e/chapter9/
    # -> Saving Variables with the pprint.pformat() Function
    # fileObj = open(path, "w")
    fileObj = path
    fileObj.write("nasdaq_data = " + pprint.pformat(data) + "\n")
    # fileObj.close()


def convert_nasdaq_data_to_df(data: dict) -> pd.DataFrame:
    # data["data"]["rows"] is a list of dictionaries.
    df = pd.DataFrame(data["data"]["rows"])
    # The marketCap column contains empty strings. So, if I do
    #   df['marketCap'] = df['marketCap'].astype('float')
    # it gives
    #   ValueError: could not convert string to float: ''
    # As a workaround, I am using pandas.to_numeric with errors='coerce'
    # which will convert any value error to NaN
    # Ref:- https://pandas.pydata.org/docs/reference/api/pandas.to_numeric.html
    df["marketCap"] = pd.to_numeric(df["marketCap"], errors="coerce")
    # df['pctchange'] is a string such as '-0.122%' . Remove the trailing '%' symbol and make it a float.
    # We cannot use
    #   df["pctchange"] = df["pctchange"].str.rstrip("%").astype(float)
    # as some of the entries in df["pctchange"] are empty strings, and it will fail with
    #   ValueError: could not convert string to float: ''
    df["pctchange"] = (
        df["pctchange"].str.rstrip("%").apply(pd.to_numeric, errors="coerce")
    )
    return df


def dump_nasdaq_df(df: pd.DataFrame, path: str):
    # When dumping the output on the command line, we do not want to print
    # extra stuff as it will interfere with downstream processing such as
    #   get_nasdaq_data.py | body grep -i NWSA
    # So, print the file information only if it is not stdout.
    if path is not sys.stdout:
        print("writing nasdaq data to", path)
    # If you try to open the csv file written without the lineterminator='\n'
    # option, in excel, shows empty lines in every alternate row. If you
    # write them with lineterminator='\n' option, then excel opens it correctly.
    df.to_csv(path, index=False, lineterminator="\n")


def get_nasdaq_df():
    data = get_nasdaq_data()
    df = convert_nasdaq_data_to_df(data)
    return df


def run_code():
    parser = create_parser()
    args = parser.parse_args()
    data = get_nasdaq_data()
    path = args.output_file

    # # Ref:- https://stackoverflow.com/questions/4028904/what-is-a-cross-platform-way-to-get-the-home-directory
    # # home = os.path.expanduser("~")
    # # path = os.path.join(home, "x", "data.py")
    # dump_raw_nasdaq_data(data, path)

    # path = os.path.join(home, 'x', 'data.csv')
    df = convert_nasdaq_data_to_df(data)
    dump_nasdaq_df(df, path)

    if path is not sys.stdout:
        path.close()


if __name__ == "__main__":
    run_code()
