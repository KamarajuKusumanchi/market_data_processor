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

# By default, the price data comes with 13 digits of precision. But I noticed
# that the numbers change slightly from run to run. I reported this as
# "https://github.com/ranaroussi/yfinance/issues/1982 - Inconsistent results
# between two successive runs".
# In the meantime, I decided to use "rounding=True" which rounds values to 2
# decimal places. This will reduce the diffs from successive runs.
daily_df = yf.download(tickers, start, end, rounding=True)
daily_file = os.path.join(user_data_dir, "daily.csv")

print(f"storing daily SPY returns in {daily_file}")
daily_df.to_csv(daily_file)


def daily_ohlc_to_month_end_ohlc(daily):
    monthly = daily.resample("ME").agg(
        {
            "Open": "first",
            "High": "max",
            "Low": "min",
            "Close": "last",
            "Adj Close": "last",
            "Volume": "sum",
        }
    )
    return monthly


monthly_df = daily_ohlc_to_month_end_ohlc(daily_df)

monthly_file = os.path.join(user_data_dir, "monthly.csv")
print(f"storing monthly SPY returns in {monthly_file}")
monthly_df.to_csv(monthly_file)
