# Sample code used to report issue
# https://github.com/ranaroussi/yfinance/issues/1982 - Inconsistent results between two successive runs

import yfinance as yf
from datetime import datetime, date

yf.enable_debug_mode()

df = yf.download(["SPY"], date(2023, 1, 1), date(2024, 7, 2))

time_stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
file_name = f"daily_{time_stamp}.csv"
print(f"writing data into {file_name}")
df.to_csv(file_name)
