# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.16.2
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

import io
import pandas as pd
data = """
Date,Open,High,Low,Close,Adj Close,Volume
2024-01-02,472.16,473.67,470.49,472.65,469.67,123623700
2024-01-03,470.43,471.19,468.17,468.79,465.84,103585900
2024-01-04,468.3,470.96,467.05,467.28,464.33,84232200
2024-01-05,467.49,470.44,466.43,467.92,464.97,86060800
2024-01-08,468.43,474.75,468.3,474.6,471.61,74879100
"""
df = pd.read_csv(io.StringIO(data))

print(df)

df.dtypes

df.index

df['Date'] = pd.to_datetime(df['Date'])
df.dtypes

df.set_index('Date', inplace=True)

print(df)

df.dtypes

df.index


