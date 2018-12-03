import pandas as pd
import numpy as np
import requests
from datetime import datetime
import sys


def get_shares_outstanding_by_chunk(tickers):
    ticker_str = ','.join(tickers)

    # sample response for
    # https://api.iextrading.com/1.0/stock/market/batch?symbols=uis,aapl&types=stats&filter=sharesOutstanding
    # {'UIS': {'stats': {'sharesOutstanding': 51013181}}, 'AAPL': {'stats': {'sharesOutstanding': 4829926000}}}
    #
    # sample response for
    # https://api.iextrading.com/1.0/stock/market/batch?symbols=uis,aapl&types=stats&filter=symbol,sharesOutstanding
    # {'UIS': {'stats': {'symbol': 'UIS', 'sharesOutstanding': 51013181}}, 'AAPL': {'stats': {'symbol': 'AAPL', 'sharesOutstanding': 4829926000}}}

    # Sample URL: https://api.iextrading.com/1.0/stock/market/batch?symbols=uis,aapl&types=stats&filter=symbol,sharesOutstanding
    url = 'https://api.iextrading.com/1.0/stock/market/batch?symbols=' + ticker_str + '&types=stats&filter=symbol,sharesOutstanding'
    # sample response:
    # {'UIS': {'stats': {'symbol': 'UIS', 'sharesOutstanding': 51013181}}, 'AAPL': {'stats': {'symbol': 'AAPL', 'sharesOutstanding': 4829926000}}}
    response = requests.get(url).json()
    # print(response)

    # convert the response to list of dictionaries
    temp = [x.get('stats') for x in response.values()]

    # put everything into a dataframe
    df = pd.DataFrame(temp)
    # print(df)
    return df


def get_shares_outstanding(tickers):
    chunk_size = 90
    chunks = [tickers[x: x + chunk_size] for x in range(0, len(tickers), chunk_size)]
    df = pd.concat((get_shares_outstanding_by_chunk(x) for x in chunks), ignore_index=True)
    df.sort_values('symbol', inplace=True)
    df.index = np.arange(len(df))
    # print(df)
    return df


if __name__ == '__main__':
    # sample usage:
    # # python <script name> uis,aapl,fb,cprt
    # tickers = sys.argv[1].split(',')

    # tickers = ['uis', 'aapl', 'fb', 'cprt']

    # sample usage:
    # echo "uis,aapl,fb,cprt" | python <script name>
    tickers = sys.stdin.readline().split(',')
    # print(tickers)

    today = datetime.today().strftime('%Y%m%d')

    df = get_shares_outstanding(tickers)
    df['date'] = today

    # set the column order
    col = ['date', 'symbol', 'sharesOutstanding']
    df = df[col]
    df.to_csv(sys.stdout, index=False)
