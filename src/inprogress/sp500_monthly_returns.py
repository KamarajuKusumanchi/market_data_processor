import os
import yfinance as yf
from datetime import datetime, date
from platformdirs import user_data_dir
from pathlib import Path

from src.utils.yfinance_utils import daily_ohlcv_to_month_end_ohlcv

appname = "market_data_processor"
version = "0.0.1"
user_data_dir = Path(
    user_data_dir(appname=appname, version=version, ensure_exists=True)
)
run_time_stamp = datetime.now().strftime("%Y%m%d_%H%M%S")

tickers = ["SPY"]
start_date = date(2024, 1, 1)
end_date = date(2024, 6, 30)

# By default, the price data comes with 13 digits of precision. But I noticed
# that the numbers change slightly from run to run. I reported this as
# "https://github.com/ranaroussi/yfinance/issues/1982 - Inconsistent results
# between two successive runs".
# In the meantime, I decided to use "rounding=True" which rounds values to 2
# decimal places. This will reduce the diffs from successive runs.
daily_df = yf.download(tickers, start=start_date, end=end_date,
                       auto_adjust=False, progress=False, rounding=True)
daily_file = os.path.join(user_data_dir, f"daily_{run_time_stamp}.csv")

print(f"storing daily SPY returns in {daily_file}")
daily_df.to_csv(daily_file)

monthly_df = daily_ohlcv_to_month_end_ohlcv(daily_df)

monthly_file = os.path.join(user_data_dir, f"monthly_{run_time_stamp}.csv")
print(f"storing monthly SPY returns in {monthly_file}")
monthly_df.to_csv(monthly_file)
