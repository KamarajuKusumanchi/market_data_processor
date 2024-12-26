import yfinance as yf
import pandas as pd
from datetime import datetime

if __name__ == "__main__":
    news = yf.Search("declares special dividend", news_count=10).news
    df = pd.DataFrame(news)
    df["providerPublishTime"] = df["providerPublishTime"].apply(datetime.fromtimestamp)
    df = df[["providerPublishTime", "relatedTickers", "title", "link", "publisher"]]
    df.to_csv(index=False)
