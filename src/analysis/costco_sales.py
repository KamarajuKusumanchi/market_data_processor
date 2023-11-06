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

import pandas as pd
file_path = '../../../market_data/costco_monthly_sales/schema_2/net_sales.txt'
df = pd.read_csv(file_path, comment='#', skipinitialspace=True)
# Get the last 12 observations.
# Todo:- This is not robust to get the rolling 12 month sales.
# For example, if there are gaps in the data, this will fail.
# Afterwards, add checks to make sure that there are no gaps in the data.
df = df.iloc[-12:]

df

df['net_sales'].sum()


