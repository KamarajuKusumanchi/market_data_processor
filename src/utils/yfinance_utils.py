def daily_ohlcv_to_month_end_ohlcv(daily):
    # 'ME' is a frequency string for "Month End"
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


def daily_ohlcv_to_weekly_ohlcv(daily):
    # 'W' is a frequency string for weekly. But it defaults to Sunday end.
    # Use 'W-FRI' for "Weekly, ending on Friday"
    weekly = daily.resample("W-FRI").agg(
        {
            "Open": "first",
            "High": "max",
            "Low": "min",
            "Close": "last",
            "Adj Close": "last",
            "Volume": "sum",
        }
    )
    return weekly
