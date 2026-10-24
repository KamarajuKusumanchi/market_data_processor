#!/usr/bin/env python3
"""
Compute the returns of a list of stocks over a given time frame.

Requirements:
    pip install yfinance pandas

Examples:
    python stock_returns.py AAPL MSFT NVDA --start 2025-01-01 --end 2025-12-31
    python stock_returns.py AAPL MSFT --period 1y
    python stock_returns.py AAPL TSLA --start 2024-01-01 --csv returns.csv
"""

import argparse
import sys
from datetime import date

import pandas as pd
import yfinance as yf


def get_returns(tickers, start=None, end=None, period=None):
    """
    Return a DataFrame with one row per ticker and columns:
        start_date, end_date, start_price, end_price, total_return_pct

    Uses adjusted close prices (auto_adjust=True, which makes the "Close"
    column the adjusted close), so dividends and splits
    are reflected in the returns (i.e. total return).

    Provide either (start, end) or period (e.g. '1mo', '6mo', '1y', '5y', 'ytd', 'max').
    """
    tickers = [t.upper().strip() for t in tickers]

    if period:
        prices = yf.download(tickers, period=period, auto_adjust=True,
                             progress=False)["Close"]
    else:
        prices = yf.download(tickers, start=start, end=end, auto_adjust=True,
                             progress=False)["Close"]

    # With a single ticker yfinance may return a Series; normalize to DataFrame
    if isinstance(prices, pd.Series):
        prices = prices.to_frame(name=tickers[0])

    rows = []
    for t in tickers:
        if t not in prices.columns:
            print(f"Warning: no data returned for {t}", file=sys.stderr)
            continue

        series = prices[t].dropna()
        if len(series) < 2:
            print(f"Warning: not enough data for {t}", file=sys.stderr)
            continue

        p0, p1 = series.iloc[0], series.iloc[-1]
        d0, d1 = series.index[0], series.index[-1]
        total = p1 / p0 - 1

        rows.append({
            "ticker": t,
            "start_date": d0.date(),
            "end_date": d1.date(),
            "start_price": round(float(p0), 2),
            "end_price": round(float(p1), 2),
            "total_return_pct": round(float(total) * 100, 2),
        })

    return pd.DataFrame(rows).set_index("ticker") if rows else pd.DataFrame()


def main():
    parser = argparse.ArgumentParser(description="Compute stock returns over a time frame.")
    parser.add_argument("tickers", nargs="+", help="Ticker symbols, e.g. AAPL MSFT")
    parser.add_argument("--start", help="Start date YYYY-MM-DD")
    parser.add_argument("--end", default=str(date.today()), help="End date YYYY-MM-DD (default: today)")
    parser.add_argument("--period", help="Alternative to start/end: 1mo, 3mo, 6mo, 1y, 5y, ytd, max")
    parser.add_argument("--csv", help="Optional path to save results as CSV")
    args = parser.parse_args()

    if not args.start and not args.period:
        parser.error("Provide either --start (with optional --end) or --period")

    df = get_returns(args.tickers, start=args.start, end=args.end, period=args.period)

    if df.empty:
        print("No results.", file=sys.stderr)
        sys.exit(1)

    df = df.sort_values("total_return_pct", ascending=False)
    print(df.to_string())

    if args.csv:
        df.to_csv(args.csv)
        print(f"\nSaved to {args.csv}")


if __name__ == "__main__":
    main()
