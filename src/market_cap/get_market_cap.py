import requests
import pandas as pd


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


def convert_nasdaq_data_to_df(data):
    df = pd.DataFrame(data["data"]["rows"])
    return df


def get_nasdaq_df():
    data = get_nasdaq_data()
    df = convert_nasdaq_data_to_df(data)
    # The marketCap column contains empty strings. So, if I do
    #   df['marketCap'] = df['marketCap'].astype('float')
    # it gives
    #   ValueError: could not convert string to float: ''
    # As a workaround, I am using pandas.to_numeric with errors='coerce'
    # which will convert any value error to NaN
    # Ref:- https://pandas.pydata.org/docs/reference/api/pandas.to_numeric.html
    df["marketCap"] = pd.to_numeric(df["marketCap"], errors="coerce")
    return df


def get_market_cap(nasdaq_df):
    """
    :param nasdaq_df: dataFrame
    :return: dataFrame
    """
    return nasdaq_df[["symbol", "marketCap"]]
    return 0


def run_code():
    nasdaq_df = get_nasdaq_df()
    market_cap = get_market_cap(nasdaq_df)
    pd.set_option("display.max_columns", None, "display.max_rows", None)
    print(market_cap.to_csv(index=False))


if __name__ == "__main__":
    run_code()
