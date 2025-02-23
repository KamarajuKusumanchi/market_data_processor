import yfinance as yf


def test_ticker_info():
    spy = yf.Ticker("SPY")
    spy_info = spy.info
    assert spy_info is not None


def test_news_search():
    news_count = 10
    news = yf.Search("declares special dividend", news_count=news_count).news
    assert len(news) == news_count
