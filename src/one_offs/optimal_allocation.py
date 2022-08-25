#! /usr/bin/env python3

# show optimal allocation between two tickers.

from datetime import date, timedelta
import pandas_datareader.data as web

def get_end_date():
    end_date = date.today()
    return end_date

def get_start_date(end_date):
    years = 1
    start_date = end_date - timedelta(days=years * 365)
    return start_date

def get_price_returns(ticker, start_date, end_date):
    ohlc = web.DataReader(ticker, 'yahoo', start=start_date, end=end_date)
    return ohlc

if __name__ == '__main__':
    # Todo: move this to a pytest
    end_date = get_end_date()
    start_date = get_start_date(end_date)
    ticker = 'COST'
    df = get_price_returns(ticker, start_date, end_date)
    print(df)