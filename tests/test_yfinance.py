import yfinance as yf
from packaging.version import Version


def test_check_version():
    # using the recipe in https://stackoverflow.com/questions/11887762/how-do-i-compare-version-numbers-in-python to compare package versions.
    installed_version = Version(yf.__version__)
    required_version = Version("0.2.61")
    assert (
        installed_version >= required_version
    ), f"Installed version of yfinance is {installed_version}. But at least version {required_version} is required."


def test_ticker_info():
    spy = yf.Ticker("SPY")
    spy_info = spy.info
    assert spy_info is not None


def test_news_search():
    news_count = 10
    # news = yf.Search("declares special dividend", news_count=news_count).news
    news = yf.Search("nvidia", news_count=news_count).news
    assert len(news) == news_count
