# Following the convention used in https://pydata.github.io/pandas-datareader/remote_data.html#yahoo-finance-data

import pandas_datareader.data as web

if __name__ == "__main__":
    df = web.get_data_yahoo("ES=F", start="2021-11-01", end="2021-11-10")
    print(df)
