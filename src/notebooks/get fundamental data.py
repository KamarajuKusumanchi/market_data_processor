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

# How to get fundamental data such as Mcap, Fcf, Ebitda, EPS for a given stock?

import yfinance as yf
import pandas as pd
info = yf.Ticker('MSFT').info

# info is a dictionary with a lot of fundamental data
info

# narrow it down to fields you are interested in
data = {key:info[key] for key in ['marketCap', 'freeCashflow', 'ebitda', 'trailingEps', 'forwardEps']}
data

# Final script
import yfinance as yf
info = yf.Ticker('MSFT').info
data = {key:info[key] for key in ['marketCap', 'freeCashflow', 'ebitda', 'trailingEps', 'forwardEps']}
data


