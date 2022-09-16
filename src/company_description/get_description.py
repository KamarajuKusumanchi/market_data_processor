#! /usr/bin/env python3
import os.path
import textwrap
import time

from finvizfinance.quote import finvizfinance

import argparse


def run_code():
    parser = create_parser()
    args = parser.parse_args()
    ticker = args.ticker
    update_cache(ticker)
    description = retrieve_cache(ticker)
    print(description, end="")


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
    file_exists = os.path.exists(file_path)
    file_age = time.time() - os.path.getmtime(file_path) if file_exists else -1
    # age_threshold = threshold in seconds to determine whether a file is new or old.
    age_threshold = 30 * 24 * 60 * 60  # 30 days
    file_is_too_old = file_age > age_threshold
    if not file_exists or file_is_too_old:
        description = get_description(ticker)
        print("writing to", file_path)
        with open(file_path, "w") as fh:
            fh.write(description)
            # Note1: all text files should end with a new line character.
            # Ref: https://stackoverflow.com/questions/729692/why-should-text-files-end-with-a-newline
            # Note 2: Do not use os.linesep as a line terminator when writing
            # files opened in text mode (the default); use a single '\n'
            # instead, on all platforms.
            # Ref: https://docs.python.org/3/library/os.html#os.linesep
            fh.write("\n")


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
