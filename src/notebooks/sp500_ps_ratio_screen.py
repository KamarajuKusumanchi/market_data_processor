# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.1
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown] editable=true slideshow={"slide_type": ""}
# Q: What percentage of sp500 companies have P/S more than 10?

# %%
import pandas as pd

# %%
df = pd.read_csv("https://raw.githubusercontent.com/datasets/s-and-p-500-companies-financials/refs/heads/main/data/constituents-financials.csv")
df

# %%
total = len(df)
gte_mask = df['Price/Sales'] >= 10
lt_mask = df['Price/Sales'] < 10
nan_mask = ~gte_mask & ~lt_mask
gte = gte_mask.sum()
lt = lt_mask.sum()
nan = nan_mask.sum()

counts_dict = {
    'total': total,
    'greater_or_equal_10': gte,
    'less_than_10': lt,
    'nan': nan,
    'pct_greater_or_equal_10': round((gte / total) * 100, 2),
    'pct_less_than_10': round((lt / total) * 100, 2),
    'pct_nan': round((nan / total) * 100, 2)
}

counts = pd.Series(counts_dict)
print(counts.to_string(dtype=False))

# %%
df['Sales'] = df['Market Cap'] / df['Price/Sales']
total_sales = df['Sales'].sum()
total_mktcap = df['Market Cap'].sum()
sales_dict = {
    'total_sales_tn_$': total_sales / 1e12,
    'total_market_cap_tn_$': total_mktcap / 1e12,
    'index_price_to_sales': round(total_mktcap / total_sales, 2)
}
sales = pd.Series(sales_dict)
print()
print(sales.to_string(dtype=False))

