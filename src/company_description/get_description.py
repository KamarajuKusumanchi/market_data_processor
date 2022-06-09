#! /usr/bin/env python3

from finvizfinance.quote import finvizfinance

import argparse


def create_parser():
    parser = argparse.ArgumentParser(
        description='Get company description from ticker'
    )
    parser.add_argument('ticker', action='store', help='ticker')
    parser.add_argument(
        "--debug", action="store_true",
        default=False, dest='debug',
        help='show debug output'
    )
    return parser


def run_code():
    parser = create_parser()
    args = parser.parse_args()
    ticker = args.ticker
    stock = finvizfinance(ticker)
    description = stock.ticker_description()
    print(description)


if __name__ == "__main__":
    run_code()
