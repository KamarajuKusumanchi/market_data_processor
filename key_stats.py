#! /usr/bin/env python3
# script to scrape data from Bloomberg website
#
# Sample usage
#  % echo "BABA" | key_stats.py
# <Todo:- provide the output here>

from bs4 import BeautifulSoup
import requests
import sys


def get_html(url):
    # Get html from url
    response = requests.get(url)
    return response.text


if __name__ == "__main__":
    symbol = sys.stdin.readline()
    symbol = symbol.strip()
    url = 'https://www.bloomberg.com/quote/' + symbol + ':US'
    html = get_html(url)
    out_file = 'bbg_' + symbol + '.txt'
    with open(out_file, 'w') as fh:
        print('writing', out_file)
        fh.write(html)

