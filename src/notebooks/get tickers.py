# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.16.4
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# today | 2023-10-02
# get a list of the 11,321 currently traded symbols from NASDAQ using
# pandas-datareader
# 
# Ref:- Machine Learning for Algorithmic Trading - Stefan Jansen - 2020 - 2nd edition.pdf -> pg-640
from pandas_datareader.nasdaq_trader import get_nasdaq_symbols
traded_symbols = get_nasdaq_symbols()

type(traded_symbols)

traded_symbols.shape

traded_symbols

tickers = traded_symbols.index.to_list()

len(tickers)

print(tickers[0:10], '...', tickers[-10:])

# remove ETFs
non_etf_tickers = traded_symbols[~traded_symbols.ETF].index.to_list()

len(non_etf_tickers)

print(non_etf_tickers[0:10], '...', non_etf_tickers[-10:])


