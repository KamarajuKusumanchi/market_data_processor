import os.path
import pandas.testing as pdt

import pandas as pd
from src.utils.yfinance_utils import daily_ohlcv_to_month_end_ohlcv


def test_daily_ohlc_to_month_end_ohlc():
    this_file = os.path.abspath(__file__)
    this_dir = os.path.dirname(this_file)
    tests_dir = os.path.dirname(os.path.dirname(this_dir))
    data_dir = os.path.join(tests_dir, "data")

    daily_file_name = os.path.join(
        data_dir, "daily_ohlc_spy_20240101_20240630_from_yahoo.csv"
    )
    daily_df = pd.read_csv(daily_file_name)
    daily_df['Date'] = pd.to_datetime(daily_df['Date'])
    daily_df.set_index("Date", inplace=True)

    monthly_df_got = daily_ohlcv_to_month_end_ohlcv(daily_df)

    monthly_file_name = os.path.join(
        data_dir, "monthly_ohlc_spy_20240101_20240630_from_yahoo.csv"
    )
    monthly_df_expected = pd.read_csv(monthly_file_name)
    monthly_df_expected["Date"] = pd.to_datetime(monthly_df_expected["Date"])
    monthly_df_expected.set_index("Date", inplace=True)
    monthly_df_expected.index.freq = pd.offsets.MonthEnd()

    pdt.assert_frame_equal(monthly_df_got, monthly_df_expected)
