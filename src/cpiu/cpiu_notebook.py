# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.14.1
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# Goal:-
# * Get the data in <https://download.bls.gov/pub/time.series/cu/cu.data.1.AllItems> as a pandas dataframe.
#
# Notes:-
# * pd.read_html(url) can't be used as it will fail with
# ```
# ValueError: No tables found
# ```
#
# * BeautifulSoup will require us to write lot of parsing code.
#
# * pd.read_fwf(url) will give wrong results. For example
# ```
# import pandas as pd
# url = 'https://download.bls.gov/pub/time.series/cu/cu.data.1.AllItems'
# df = pd.read_fwf(url)
# df[(df['series_id'] == 'CUUR0000SA0') & (df['year'] == 2022) & (df['period'] == 'M08')]
# ```
# shows that the CPI-U value for August 2022 is 6.171 but should actually be 296.171 instead.
# ```
#         series_id  year period  value  footnote_codes
# 3757  CUUR0000SA0  2022    M08  6.171             NaN
# ```
#
# * pd.read_csv(url, delimiter='\t') is not ideal but good enough.
# For example, it adds extra white spaces in column names and series_id values etc., and will require further processing.
#
# Expected column names:
# ```
# ['series_id', 'year', 'period', 'value', 'footnote_codes']
# ```
# output from pd.read_csv:
# ```
# ['series_id        ', 'year', 'period', '       value', 'footnote_codes']
# ```

import pandas as pd

url = 'https://download.bls.gov/pub/time.series/cu/cu.data.1.AllItems'

df = pd.read_csv(url, delimiter='\t')

# Some of the columns have white spaces in their names.
# These white spaces are showing up either at the beginning or at the end.
df.columns

# Strip the white spaces in column names
df.columns = df.columns.str.strip()

df.columns

df.shape

df.head()

df.tail()

# The series_id values have trailing white spaces.
# For example, we have 'CUUR0000SA0      '. But we want them as 'CUUR0000SA0'
df[(df['series_id'] == 'CUUR0000SA0      ') & (df['year'] == 2022) & (df['period'] == 'M08')]

# Strip the white spaces in series_id column.
df['series_id'] = df['series_id'].str.strip()
df[(df['series_id'] == 'CUUR0000SA0') & (df['year'] == 2022) & (df['period'] == 'M08')]

# verify that we get same values as shown in https://www.bls.gov/regions/mid-atlantic/data/consumerpriceindexhistorical_us_table.htm
cpiu_id = 'CUUR0000SA0'
df[(df['series_id'] == cpiu_id) & (df['year'] == 2021)]

# period = M13 is just the annual average.
year_of_interest = 2020
average_cpu1 = df[(df['series_id'] == cpiu_id) & (df['year'] == year_of_interest) & (df['period'] == 'M13')]['value'].values[0]
average_cpu2 = df[(df['series_id'] == cpiu_id) & (df['year'] == year_of_interest) & (df['period'] != 'M13')]['value'].mean()
(average_cpu1, average_cpu2, average_cpu1 - average_cpu2)

# Get cpiu data without the (period = M13) entries
cpiu = df[(df['series_id'] == cpiu_id) & (df['period'] != 'M13')].copy()

cpiu[(cpiu['year'] == 2021)]

cpiu['month'] = cpiu['period'].str[-2:].astype(int)
cpiu['date'] = cpiu['year'].astype(str) + '-' + cpiu['period'].str[-2:]

cpiu

pd.__version__

(cpiu['value'].pct_change(12) * 100).dropna()
