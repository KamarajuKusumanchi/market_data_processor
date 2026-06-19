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
print(f"Run at: {pd.Timestamp.now()}")

# %%
df = pd.read_csv("https://raw.githubusercontent.com/datasets/s-and-p-500-companies-financials/refs/heads/main/data/constituents-financials.csv")
df

# %%
total = len(df)
gte_mask = df['Price/Sales'] >= 10
lt_mask = df['Price/Sales'] < 10
nan_mask = df['Price/Sales'].isna()
gte = gte_mask.sum()
lt = lt_mask.sum()
nan = nan_mask.sum()

assert total == gte + lt + nan, (
    f"counts don't add up: total={total}, gte={gte}, lt={lt}, nan={nan}"
)

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
print("==== S&P 500 P/S Ratio Distribution ====")
print(counts.to_string(dtype=False))

# %%
# Restrict both market cap and sales to the same population (companies with a
# valid Price/Sales value). Mixing all-company market cap with sales summed
# only over non-NaN P/S rows understates the denominator and inflates the
# resulting index-level ratio.

valid_mask = df['Price/Sales'].notna()
excluded = (~valid_mask).sum()
excluded_mktcap = df.loc[~valid_mask, 'Market Cap'].sum()

df['Sales'] = df['Market Cap'] / df['Price/Sales']
total_sales = df.loc[valid_mask, 'Sales'].sum()
total_mktcap = df.loc[valid_mask, 'Market Cap'].sum()

sales_dict = {
    'total_sales_tn_$': round(total_sales / 1e12, 3),
    'total_market_cap_tn_$': round(total_mktcap / 1e12, 3),
    'index_price_to_sales': round(total_mktcap / total_sales, 2),
    'excluded_companies_nan_ps': excluded,
    'excluded_market_cap_tn_$': round(excluded_mktcap / 1e12, 3)
}
sales = pd.Series(sales_dict)
print()
print("==== S&P 500 Aggregate Financials & Index P/S ====")
print(sales.to_string(dtype=False))

