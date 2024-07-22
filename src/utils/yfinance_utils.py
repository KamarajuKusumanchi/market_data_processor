def daily_ohlcv_to_month_end_ohlcv(daily):
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
