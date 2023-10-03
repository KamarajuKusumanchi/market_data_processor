# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.15.2
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# today | 2023-10-02
# get ticker info for all the currently traded symbols from NASDAQ using
# pandas-datareader
# 
# Ref:- Machine Learning for Algorithmic Trading - Stefan Jansen - 2020 - 2nd edition.pdf -> pg-640
from pandas_datareader.nasdaq_trader import get_nasdaq_symbols
traded_symbols = get_nasdaq_symbols()
import yfinance as yf
tickers = yf.Tickers(traded_symbols[~traded_symbols.ETF].index.to_list())

tickers = traded_symbols.index.to_list()

[ticker for ticker in tickers if isinstance(ticker, float)]

import numpy as np
traded_symbols.loc[np.nan]


