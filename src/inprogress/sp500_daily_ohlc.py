# Sample code used to report issue
# "https://github.com/ranaroussi/yfinance/issues/1982 - Inconsistent results
# between two successive runs"

import yfinance as yf
from datetime import datetime, date

# yf.enable_debug_mode()

# df = yf.download(["SPY"], date(2023, 1, 1), date(2024, 7, 2))
# auto_adjust = True
auto_adjust = False
df = yf.download(["SPY"], start=date(2023, 1, 1), end=date(2024, 7, 2), auto_adjust=auto_adjust, progress=False)

time_stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
file_name = f"daily_auto_adjust_{auto_adjust}_{time_stamp}.csv"
print(f"writing data into {file_name}")
df.to_csv(file_name)
