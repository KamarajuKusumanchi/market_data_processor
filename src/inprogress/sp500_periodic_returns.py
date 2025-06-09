#! /usr/bin/env python

# The term "periodic returns" encompasses things like monthly and weekly returns.

import os
import yfinance as yf
from datetime import datetime, date
from platformdirs import user_data_dir
from pathlib import Path

import project_root
from src.utils.yfinance_utils import daily_ohlcv_to_month_end_ohlcv, daily_ohlcv_to_weekly_ohlcv

appname = "market_data_processor"
version = "0.0.1"
user_data_dir = Path(
    user_data_dir(appname=appname, version=version, ensure_exists=True)
)
run_time_stamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# asof | 2025-04-08
# expense ratio of SPY is 9.45 bps [1] and that of VOO is 3 bps [2]. So it is
# better to buy VOO than SPY.
# 
# [1] - https://www.ssga.com/us/en/intermediary/etfs/spdr-sp-500-etf-trust-spy
# [2] - https://investor.vanguard.com/investment-products/etfs/profile/voo

tickers = ["VOO"]
# tickers = ["SPY"]
start_date = date(2024, 12, 1)
end_date = date(2025, 6, 3)

# By default, the price data comes with 13 digits of precision. But I noticed
# that the numbers change slightly from run to run. I reported this as
# "https://github.com/ranaroussi/yfinance/issues/1982 - Inconsistent results
# between two successive runs".
# In the meantime, I decided to use "rounding=True" which rounds values to 2
# decimal places. This will reduce the diffs from successive runs.
daily_df = yf.download(tickers, start=start_date, end=end_date,
                       auto_adjust=False, progress=False, rounding=True)

# This gives a dataframe with Multi-Level columns
# Flatten it using the recipe in https://stackoverflow.com/questions/63107594/how-to-deal-with-multi-level-column-names-downloaded-with-yfinance/63107801#63107801
daily_df = daily_df.stack(level=1).rename_axis(['Date', 'Ticker']).reset_index(level=1)

daily_file = os.path.join(user_data_dir, f"daily_{run_time_stamp}.csv")

print(f"storing daily returns in {daily_file}")
daily_df.to_csv(daily_file)

monthly_df = daily_ohlcv_to_month_end_ohlcv(daily_df)
monthly_file = os.path.join(user_data_dir, f"monthly_{run_time_stamp}.csv")
print(f"storing monthly returns in {monthly_file}")
monthly_df.to_csv(monthly_file)

weekly_df = daily_ohlcv_to_weekly_ohlcv(daily_df)
weekly_file = os.path.join(user_data_dir, f"weekly_{run_time_stamp}.csv")
print(f"stroing weekly returns in {weekly_file}")
weekly_df.to_csv(weekly_file)
