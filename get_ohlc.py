#! /usr/bin/env python3
# Get open, close, low, high prices of a stock.
import argparse
import copy
import pandas_datareader.data as web
from datetime import datetime
from dateutil.relativedelta import relativedelta


def get_ohlc(ticker, start, end):
    df = web.DataReader(ticker, 'iex', start, end)
    return df


def parse_arguments():
    parser = argparse.ArgumentParser()
    # parser.add_argument('-t', '--ticker', required=True, help='Ticker')
    parser.add_argument('ticker', help='Ticker')

    parser.add_argument('-sdt', '--start_date', default=None,
                        help='start date')
    parser.add_argument('-edt', '--end_date', default=None,
                        help='end date')
    parser.add_argument('--period', default=None, type=int,
                        help='number of days')
    options = parser.parse_args()
    return options


def update_start_and_end_dates(options):
    # Get the start and end dates based on the options provided by the user.
    # For example if user specified start date and period, we will use that
    # information to compute the end date etc.,
    #
    # options will be overwritten with new start and end dates as necessary.
    if options.start_date is not None:
        options.start_date = get_datetime(options.start_date)
    if options.end_date is not None:
        options.end_date = get_datetime(options.end_date)

    t1 = datetime.today()
    ndays = 31

    if options.start_date is None:
        if options.end_date is None:
            if options.period is None:
                options.period = ndays
            options.end_date = t1
        options.start_date = (options.end_date
                              + relativedelta(days=-options.period))
    else:
        if options.end_date is None:
            if options.period is None:
                options.period = ndays
            options.end_date = (options.start_date
                                + relativedelta(days=options.period))

    if options.period and \
       (options.end_date - options.start_date).days != options.period:
        print(options)
        print('Difference between end date and start_date =',
              (options.end_date - options.start_date).days,
              'is not equal to', options.period)
        raise ValueError('Inconsistent set of options.')


def get_datetime(a):
    # Handle YYYY-MM-DD
    dt_Ymd = a.replace('-', '')
    return datetime.strptime(dt_Ymd, '%Y%m%d')


if __name__ == '__main__':
    orig_options = parse_arguments()
    options = copy.deepcopy(orig_options)
    update_start_and_end_dates(options)
    df = get_ohlc(options.ticker, options.start_date, options.end_date)
    print(df.reset_index().to_string(index=False))
