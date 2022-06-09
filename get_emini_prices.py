import pandas_datareader as pdr

if __name__ == '__main__':
    df = pdr.data.get_data_yahoo('ES=F', start='2021-11-01', end='2021-11-10')
    print(df)