#! /usr/bin/env python3
# script to get last price from IEX
#
# Sample usage
# Todo: Fill later

import requests
import sys

# See https://github.com/ilemus/fundamentals/blob/master/src/retrieve/iextrading.py
# It contains a lot of functions to retrieve data from IEX

class IexData:
    ROOT_URL = 'https://api.iextrading.com/1.0/'

    # https://iextrading.com/developer/docs/#quote
    def get_quote(self, symbol):
        url = self.ROOT_URL + '/stock/' + symbol + '/quote?displayPercent=true'
        request = requests.get(url)
        # return empty dictionary if an error occurs
        if request.status_code > 299 or request.status_code < 200:
            print('Error retrieving quotes: ' + request.status_code)
            return {}
        return request.json()

class Display:
    # iex_data = IexData()

    def quote(self, data):
        # data = self.iex_data.get_quote(symbol)
        if not data:
            print('Error: could not read quotes')
            return
        # print(data)

        # fields = ['symbol', 'companyName', 'sector', 'latestPrice', 'change',
        #           'changePercent', 'latestVolume', 'avgTotalVolume',
        #           'marketCap', 'ytdChange']
        # for field in fields:
        #     print('{}: {}'.format(field, data[field]))

        print('Name: {}'.format(data['companyName']))
        print('Price: ${}'.format(data['latestPrice']))
        print('Change: {}%'.format(data['changePercent']))

if __name__ == '__main__':
    iex_data = IexData()
    symbol = sys.argv[1]
    data = iex_data.get_quote(symbol)
    display = Display()
    display.quote(data)
