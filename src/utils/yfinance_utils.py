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
