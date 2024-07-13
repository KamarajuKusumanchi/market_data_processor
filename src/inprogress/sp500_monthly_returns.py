import os
import yfinance as yf
from datetime import date
from platformdirs import user_data_dir
from pathlib import Path

appname = "market_data_processor"
version = "0.0.1"
user_data_dir = Path(
    user_data_dir(appname=appname, version=version, ensure_exists=True)
)

tickers = ["SPY"]
start = date(2023, 1, 1)
end = date(2024, 7, 2)
daily_df = yf.download(tickers, start, end)
daily_file = os.path.join(user_data_dir, "daily.csv")

print(f"storing daily SPY returns in {daily_file}")
daily_df.to_csv(daily_file)


monthly_df = daily_df.resample("ME").agg(
    {
        "Open": "first",
        "High": "max",
        "Low": "min",
        "Close": "last",
        "Adj Close": "last",
        "Volume": "sum",
    }
)
monthly_file = os.path.join(user_data_dir, "monthly.csv")
print(f"storing monthly SPY returns in {monthly_file}")
monthly_df.to_csv(monthly_file)
