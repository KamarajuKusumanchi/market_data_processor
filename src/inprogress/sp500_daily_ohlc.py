import yfinance as yf
from datetime import datetime, date
df = yf.download(["SPY"], date(2024, 1, 1), date(2024, 3, 31))
time_stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
file_name = f"daily_{time_stamp}.csv"
df.to_csv(file_name)