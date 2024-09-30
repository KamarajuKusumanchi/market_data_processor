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

# Goal:
# Plot the support and resistance levels for a given stock.
#
# Methodology: Using https://www.investopedia.com/trading/using-pivot-points-for-predictions/
#
# Let H, L, C denote previous day's high, low, close prices.
# Then define
#
# Pivot point: PP = (H + L + C)/3
#
# Support 1: S1 = 2 PP - H
#
# Resistance 1: R1 = 2 PP - L
#
# See also:
# * https://www.investopedia.com/trading/using-pivot-points-for-predictions/ - gives formulas for other things such as S2, R2
# * "Algorithmic Trading with Interactive Brokers - Matthew Scarpino" -> 14.4.1 Computing Support and Resistance - discusses the same approach outlined in https://www.investopedia.com/trading/using-pivot-points-for-predictions/
#
# tags | how to compute support and resistance levels
#
# Credits:
# * https://github.com/Aditya-dom/Quantfinance-with-backtesting/blob/main/fy/technical_indicators/pivot_point.py
#   * initial version of the code is copied from here.
#   * computes other things such as S2, R2, S3, R3
#
# <!---
# Notes to self:
# * https://github.com/Aditya-dom/Quantfinance-with-backtesting/blob/main/fy/technical_indicators/pivot_point.py
#   * Questions:
#     * After computing PP, S1, R1 etc., it does not shift the data to the next day. Should not we do that?
#     * S1, R1 are computed using unadjusted values. But it them along with "Adj Close". Should not we do that with "Close" instead?
# --->
#
# Todo:
# * S1, R1 are computed using unadjusted (H, L, C). Is that correct? or should we use adjusted (H, L, C)?

# +
import yfinance as yf
from datetime import datetime, date
import pandas as pd

df = yf.download(
    ["SPY"],
    start=date(2024, 8, 1),
    end=date(2024, 8, 31),
    auto_adjust=False,
    progress=False,
    rounding=True
)
df
# -

PP = (df['High'] + df['Low'] + df['Close'])/3
S1 = 2 * PP - df['High']
R1 = 2 * PP - df['Low']
# psr stands for pivot point, support, resistance
psr = {'PP': PP, 'S1': S1, 'R1': R1}
PSR = pd.DataFrame(psr).shift()
PSR

df2 = df.join(PSR).dropna()
df2

# Todo: Should we plot 'Close' or 'Adj Close' here?
plot = df2[['Close', 'S1', 'R1']].plot(grid=True, title='support and resistance levels')


