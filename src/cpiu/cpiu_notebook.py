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
# * BeautifulSoup will require us to write lot of code.
#
# * pd.read_fwf(url) will give wrong results. For example
# ```
# import pandas as pd
# url = 'https://download.bls.gov/pub/time.series/cu/cu.data.1.AllItems'
# df = pd.read_fwf(url)
# df[(df['series_id'] == 'CUUR0000SA0') & (df['year'] == 2022) & (df['period'] == 'M08')]
# ```
# will give
# ```
#         series_id  year period  value  footnote_codes
# 3757  CUUR0000SA0  2022    M08  6.171             NaN
# ```
# The value should be 296.171 instead of 6.171 (above)
#
# * pd.read_csv(url, delimiter='\t') is not ideal. It parses the values correctly.
# But it will give column names as
# ```
# ['series_id        ', 'year', 'period', '       value',       'footnote_codes']
# ```
# which will require further processing.

import pandas as pd

url = 'https://download.bls.gov/pub/time.series/cu/cu.data.1.AllItems'

df = pd.read_csv(url, delimiter='\t')

# Some of the columns have white spaces  in their names.
# These white spaces are showing up either at the beginning or at the end.
df.columns

# Strip the white spaces in column names
df.columns = df.columns.str.strip()

df.columns

df.shape

df.head()

# The series_id values have trailing white spaces.
# For example, we have 'CUUR0000SA0      '. But we want them as 'CUUR0000SA0'
df[(df['series_id'] == 'CUUR0000SA0      ') & (df['year'] == 2022) & (df['period'] == 'M08')]

# Strip the white spaces in series_id column.
df['series_id'] = df['series_id'].str.strip()
df[(df['series_id'] == 'CUUR0000SA0') & (df['year'] == 2022) & (df['period'] == 'M08')]

# verify that we get same values as shown in https://www.bls.gov/regions/mid-atlantic/data/consumerpriceindexhistorical_us_table.htm
cpiu_id = 'CUUR0000SA0'
df[(df['series_id'] == cpiu_id) & (df['year'] == 2022)]


