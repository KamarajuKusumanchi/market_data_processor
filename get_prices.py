# get historical stock prices
import pandas_datareader as web
from datetime import date, timedelta


def get_yahoo_prices(ticker, start_date=None, end_date=None):
    # Todo:- add test case for this
    if end_date is None:
        end_date = date.today()
    if start_date is None:
        start_date = end_date - timedelta(days=30)

    return web.DataReader(ticker, 'yahoo', start_date, end_date)


def get_recent_prices(ticker, ndays=30):
    # Todo:- add test case for this
    end_date = date.today()
    start_date = end_date - timedelta(days=ndays)
    return web.DataReader(ticker, 'yahoo', start_date, end_date)


if __name__ == "__main__":
    pass
