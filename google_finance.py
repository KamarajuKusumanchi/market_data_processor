# Get data from google finance
import pandas as pd
import urllib


def run_query(param):
    '''
    :param param: dictionary of parameters
    For example,
        param = {'q': 'WMT',
                 'startdate': '2017-11-14',
                 'enddate': '2017-11-15',
                 'output': 'csv'}
    :return: dafaframe containing all the data
    '''
    base_url = 'https://finance.google.com/finance/historical'
    full_url = base_url + '?' + urllib.parse.urlencode(param)
    output = param.get('output', None)

    df = pd.DataFrame()
    if output == 'csv':
        df = pd.read_csv(full_url)
        # The date is returned in dd-mon-yy format. Convert it to
        # datetime format.
        df['Date'] = pd.to_datetime(df['Date'], format='%d-%b-%y')
        df['Ticker'] = param.get('q', None)
    else:
        print("Only csv output is supported. But output is set to", output)
    return df

if __name__ == "__main__":
    run_query()
