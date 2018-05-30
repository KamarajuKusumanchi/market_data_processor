#! /usr/bin/env python3
# script to scrape data from Nasdaq website
#
# Original version is from
# https://github.com/IST256/learn-python/blob/master/content/lessons/14/End-To-End-Example/ETEE-GetNASDAQStockPrice.ipynb
#
# Sample usage
#  % python3 last_sale.py AAPL
# Name: Apple Inc. Common Stock Quote & Summary Data
# Price: $175.4535
# Change: 1.44%
#
#  % python3 last_sale.py AAPL
# Name: Apple Inc. Common Stock Quote & Summary Data
# Price: $175.36
# Change: 1.49%
#
#  % python3 last_sale.py MSFT
# Name: Microsoft Corporation Common Stock Quote & Summary Data
# Price: $92.67
# Change: 2.04%

from bs4 import BeautifulSoup
import requests
import sys


def get_html(url):
    # Get html from url
    response = requests.get(url)
    return response.text


def dump_string(str, fname):
    with open(fname, 'w') as fh:
        fh.write(str)


def extract_info(html):
    # take html extract faculty info return list of dictionaries
    soup = BeautifulSoup(html, "lxml")
    stock = {
        "name": soup.select("div#qwidget_pageheader h1")[0].text,
        "price": soup.select("div#qwidget_lastsale")[0].text,
    }
    # For percentage change, the direction (whether a stock went up or down) is
    # encoded in the widget color.
    # <div id="qwidget_percent" class="qwidget-percent qwidget-Green"
    #  style="white-space:nowrap">20.41%</div>
    # <div id="qwidget_percent" class="qwidget-percent qwidget-Red"
    #  style="white-space:nowrap">0.21%</div
    qwidget_percent = soup.select("div#qwidget_percent")[0]
    pct_change = qwidget_percent.text
    if 'qwidget-Red' in qwidget_percent.get('class'):
        pct_change = '-' + pct_change
    stock['pct_change'] = pct_change

    return stock


if __name__ == "__main__":
    # symbol = input("Enter Stock Symbol: ")
    symbol = sys.argv[1]
    url = 'http://www.nasdaq.com/symbol/' + symbol
    html = get_html(url)
    # out_file = 'nasdaq_symbol_' + symbol + '.txt'
    # with open(out_file, 'w') as fh:
    #     print('writing', out_file)
    #     fh.write(html)
    result = extract_info(html)
    print("Name: %s" % result["name"])
    print("Price: %s" % result["price"])
    print("Change: %s" % result["pct_change"])
