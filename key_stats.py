#! /usr/bin/env python3
# script to scrape data from Bloomberg website
#
# Sample usage
#  % echo "BABA" | key_stats.py
# <Todo:- provide the output here>

from bs4 import BeautifulSoup
import requests
import sys
import re
import json
import pandas as pd


def get_html(url):
    # Get html from url
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
    header = {'User-Agent': user_agent}
    response = requests.get(url, headers=header)
    return response.text


def print_full(df):
    # To print all columns in the same line
    # See https://stackoverflow.com/a/25415404/6305733
    pd.set_option('display.expand_frame_repr', False)
    print(df)


def extract_info(html):
    # Todo:- Add a test case for this function.
    soup = BeautifulSoup(html, "lxml")
    body = soup.find("body")
    script = body.find("script", {"type": "text/javascript"})
    regex = r"window.__bloomberg__.bootstrapData\s*=\s*(.*);"
    data = json.loads(re.search(regex, script.get_text()).group(1))
    df = pd.DataFrame.from_dict(data['keyStats']['keyStatsList'])
    return df


if __name__ == "__main__":
    symbol = sys.stdin.readline()
    symbol = symbol.strip()
    url = 'https://www.bloomberg.com/quote/' + symbol + ':US'
    html = get_html(url)
    out_file = 'bbg_' + symbol + '.txt'
    with open(out_file, 'w') as fh:
        print('writing', out_file)
        fh.write(html)
    # # read the data back
    # with open(out_file, "r") as fh:
    #     html = fh.read()
    result = extract_info(html)
    print_full(result)
