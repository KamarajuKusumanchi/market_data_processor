import unittest
import pandas as pd
try:
    import pandas.testing as pdt
except ImportError:
    # import pandas.testing is not working in pandas 0.19.2 which comes as the
    # default version in Debian Stretch (stable) via the python3-pandas
    # 0.19.2-5.1 package.
    import pandas.util.testing as pdt

import google_finance


class googleFinanceTestCase(unittest.TestCase):
    # @unittest.skip("Not working. Google may have changed api?")
    def test_run_query(self):
        '''Test the results of a simple query'''
        param = {'q': 'WMT',
                 'startdate': '2017-11-14',
                 'enddate': '2017-11-15',
                 'output': 'csv'}
        result = google_finance.run_query(param)
        expected = pd.DataFrame({'Date': ['2017-11-15', '2017-11-14'],
                                 'Open': [90.34, 90.70],
                                 'High': [90.85, 91.20],
                                 'Low': [89.65, 90.18],
                                 'Close': [89.83, 91.09],
                                 'Volume': [8433438, 9834133],
                                 'Ticker': ['WMT', 'WMT']})
        expected['Date'] = pd.to_datetime(expected['Date'], format='%Y-%m-%d')
        pdt.assert_frame_equal(result, expected, check_like=True)
