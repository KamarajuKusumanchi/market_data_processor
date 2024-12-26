#! /usr/bin/env python

# Sample usage:
#  % pwd
# /home/rajulocal/work/github/market_data_processor/src/utils
#  % mkdir -p ../../../market_data/special_dividends
#  % ./special_dividends.py > ../../../market_data/special_dividends/special_dividends.csv

import yfinance as yf
import pandas as pd
from datetime import datetime
import sys

if __name__ == "__main__":
    news = yf.Search("declares special dividend", news_count=10).news
    df = pd.DataFrame(news)
    df["providerPublishTime"] = df["providerPublishTime"].apply(datetime.fromtimestamp)
    df = df[["providerPublishTime", "relatedTickers", "title", "link", "publisher"]]
    df.to_csv(sys.stdout, index=False)
