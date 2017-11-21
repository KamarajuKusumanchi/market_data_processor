# Get data from google finance
import pandas as pd
import urllib


def run_query(params):
    '''
    :param params: dictionary of parameters
    For example {'q': 'WMT', 'startdate': '2017-11-01',
    'enddate': '2017-11-15', 'output': 'csv'}
    :return: dafaframe containing all the data
    '''
    # Todo:- Add a test case for this.
    base_url = 'https://finance.google.com/finance/historical'
    full_url = base_url + '?' + urllib.parse.urlencode(params)
    output = params.get('output', None)

    df = pd.DataFrame()
    if output == 'csv':
        df = pd.read_csv(full_url)
        # The date is returned in dd-mon-yy format. Change it to
        # yyyy-mm-dd format.
        df['Date'] = pd.to_datetime(df['Date'], format='%d-%b-%y')
        df['Ticker'] = params.get('q', None)
    else:
        print("Only csv output is supported. But output is set to", output)
    return df

if __name__ == "__main__":
    run_query()
