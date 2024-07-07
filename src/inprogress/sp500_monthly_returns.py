import yfinance as yf
from datetime import date

tickers = ["SPY"]
start = date(2023, 1, 1)
end = date(2024, 7, 2)
daily = yf.download(tickers, start, end)
# print(daily)
print("storing daily SPY returns in daily.csv")
daily.to_csv("daily.csv")


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
# print(monthly)
print("storing monthly SPY returns in monthly.csv")
monthly.to_csv("monthly.csv")
