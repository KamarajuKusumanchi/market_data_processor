#! /usr/bin/env python3
import os
import pprint

import pandas as pd
import requests


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


def dump_nasdaq_data(data: dict):
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


def run_code():
    nasdaq_data = get_nasdaq_data()
    dump_nasdaq_data(nasdaq_data)


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


if __name__ == "__main__":
    run_code()
