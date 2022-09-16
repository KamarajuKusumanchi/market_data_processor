#! /usr/bin/env python3
import os.path
import textwrap

from finvizfinance.quote import finvizfinance

import argparse


def run_code():
    parser = create_parser()
    args = parser.parse_args()
    ticker = args.ticker
    update_cache(ticker)
    description = retrieve_cache(ticker)
    print(description)


def create_parser():
    parser = argparse.ArgumentParser(description="Get company description from ticker")
    parser.add_argument("ticker", action="store", help="ticker")
    parser.add_argument(
        "--debug",
        action="store_true",
        default=False,
        dest="debug",
        help="show debug output",
    )
    return parser


def update_cache(ticker):
    cache_dir = get_cache_dir()
    file_name = get_cache_file_name(ticker)
    file_path = os.path.join(cache_dir, file_name)
    if not os.path.exists(file_path):
        description = get_description(ticker)
        print("writing to", file_path)
        with open(file_path, "w") as fh:
            fh.write(description)


def retrieve_cache(ticker):
    cache_dir = get_cache_dir()
    file_name = get_cache_file_name(ticker)
    file_path = os.path.join(cache_dir, file_name)
    print("reding from", file_path)
    with open(file_path, "r") as fh:
        description = fh.read()
    return description


def get_cache_dir():
    this_file = os.path.abspath(__file__)
    proj_dir = os.path.dirname(os.path.dirname(os.path.dirname(this_file)))
    cache_dir = os.path.join(os.path.dirname(proj_dir), "company_description", "public")
    return cache_dir


def get_cache_file_name(ticker):
    file_name = ticker + ".txt"
    return file_name


def get_description(ticker):
    stock = finvizfinance(ticker)
    raw_description = stock.ticker_description()
    description = format_line(raw_description)
    return description


def format_line(line):
    # To make the output look same as what we get from vim's gq command.
    width = 79
    lines = textwrap.fill(line, width)
    return lines


if __name__ == "__main__":
    run_code()
