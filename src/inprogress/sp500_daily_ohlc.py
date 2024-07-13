import yfinance as yf
from datetime import datetime, date

# data is not reproducible for these date ranges
# df = yf.download(["SPY"], date(2023, 12, 1), date(2024, 5, 31))
# df = yf.download(["SPY"], date(2023, 12, 1), date(2024, 4, 30))
# df = yf.download(["SPY"], date(2023, 12, 1), date(2024, 2, 29))
# df = yf.download(["SPY"], date(2023, 12, 1), date(2024, 1, 31))
# df = yf.download(["SPY"], date(2023, 12, 1), date(2024, 1, 15))
# df = yf.download(["SPY"], date(2024, 1, 1), date(2024, 1, 15))
# df = yf.download(["SPY"], date(2024, 1, 8), date(2024, 1, 15))
df = yf.download(["SPY"], date(2024, 1, 8), date(2024, 1, 11))

# data is reproducible for these date ranges
# df = yf.download(["SPY"], date(2024, 1, 1), date(2024, 5, 31))
# df = yf.download(["SPY"], date(2023, 12, 15), date(2024, 1, 15))
# df = yf.download(["SPY"], date(2024, 1, 1), date(2024, 1, 8))

time_stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
file_name = f"daily_{time_stamp}.csv"
print(f"writing data into {file_name}")
df.to_csv(file_name)
