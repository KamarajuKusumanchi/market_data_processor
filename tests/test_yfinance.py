import yfinance as yf


def test_ticker_info():
    spy = yf.Ticker("SPY")
    spy_info = spy.info
    assert spy_info is not None
