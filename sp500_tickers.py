#! /usr/bin/env python3

'''Script to get the list of S&P 500 tickers'''
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import sys


def get_sp500_table(filter_columns=None):
    """
    Parse a wikipedia article to extract information on the S&P 500 companies
    :param filter_columns: columns to filter. It can either be a list or
    a string or None.
    * List - list of columns to filter
    * string - filter that column
    * None - return all columns
    :return: By default, returns a Data Frame containing company tickers,
    names, sector, information etc., of all the S&P 500 companies. If
    filter_columns is supplied it returns only those columns.
    """
    # Todo:- Add a test case for this function.
    url = "https://en.wikipedia.org/wiki/List_of_S&P_500_companies"
    resp = requests.get(url)
    # resp.text is the content of the response in unicode.
    soup = BeautifulSoup(resp.text, "lxml")
    table = soup.find('table', {'class': 'wikitable sortable'})
    # Each row in the table is limited by <tr>..</tr>.
    rows = table.findAll('tr')
    # The first row is the header of the table. Each cell in the header is
    # delimited by <th>..</th>
    columns = [x.text for x in rows[0].findAll('th')]
    # The cells in each row are delimited by <td>..</td>
    df = pd.DataFrame([[cell.text
                        for cell in row.findAll('td')]
                       for row in rows[1:]],
                      columns=columns)

    if filter_columns is not None:
        if isinstance(filter_columns, str):
            filter_columns = [filter_columns]
        return df[filter_columns]
    return df


def get_sp500_tickers():
    '''Get the list of S&P 500 tickers'''
    coi = ['Symbol']
    return get_sp500_table(coi).tolist()


def get_sp500_df():
    coi = 'Symbol'
    table = get_sp500_table(coi)
    today = datetime.today().strftime('%Y%m%d')
    # This will give a dataframe with YYYYMMDD as the row index, tickers as
    # columns.
    tickers = table.sort_values(by=coi)\
        .transpose()\
        .rename({coi: today})
    return tickers


if __name__ == "__main__":
    # from time import time
    # start = time()

    # print(*get_sp500_tickers(), sep='\n')
    tickers = get_sp500_df()
    tickers.to_csv(sys.stdout, header=False)

    # print("time taken = ", time()-start, " s")
