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

# Status:
# work in progress.
#
# Goal:-
# * Get the data in <https://download.bls.gov/pub/time.series/cu/cu.data.1.AllItems> as a pandas dataframe.
#
#
# Notes:-
# * pd.read_html() can't be used as it will fail with
#
# ValueError: No tables found
#
# * BeautifulSoup will require lot of code.
#
# * pd.read_csv(url, delimiter='\t') will give column names as ```['series_id        ', 'year', 'period', '       value',       'footnote_codes']``` and will require further processing.

import pandas as pd

url = 'https://download.bls.gov/pub/time.series/cu/cu.data.1.AllItems'

df = pd.read_fwf(url)

df.shape

df.head()

cpiu_id = ['CUUR0000SA0']
df[df['series_id'].isin(cpiu_id)]

df[(df['series_id'] == cpiu_id[0]) & (df['year'] == 2022)]

df_csv = pd.read_csv(url, delimiter='\t')
df_csv.columns = df_csv.columns.str.strip()
df_csv.columns

df_csv.head()

df_csv[df_csv['series_id'].isin(cpiu_id)]

df_csv[(df_csv['series_id'] == cpiu_id[0]) & (df_csv['year'] == 2022)]


