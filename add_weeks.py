#! /usr/bin/env python

import sys
from datetime import datetime, timedelta
import argparse
import pandas as pd

# Script to add a given number of weeks to a date.

# Todo:-
# Add test cases with sample input and output.
# Sample input and output can be found in expected_output.txt


def parse_arguments(args):
    parser = argparse.ArgumentParser(
        description='Add a given number of weeks to a date.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "dt", action='store',
        help='date'
    )
    parser.add_argument(
        "offset", action='store',
        nargs='+',
        help='offset'
    )
    parser.add_argument(
        "--debug", action="store_true",
        default=False, dest='debug',
        help='show debug output'
    )
    res = parser.parse_args()
    if res.debug:
        print(res)
    return res


def run_code():
    args = parse_arguments(sys.argv[1:])

    debug = args.debug

    dt = args.dt
    if len(dt) == 8:
        fmt = '%Y%m%d'
    elif len(dt) == 10:
        fmt = '%Y-%m-%d'
    else:
        print('date = ', dt, ' is in unrecognizable format.')
        sys.exit(1)

    offset = [int(x) for x in args.offset]
    if debug:
        print(offset)
    df = pd.DataFrame({'offset': offset})
    df['cum_offset'] = df['offset'].cumsum()
    df['date'] = datetime.strptime(dt, fmt) + \
        pd.to_timedelta(df['cum_offset'], 'w')
    if debug:
        print(df)
    print(df['date'].dt.strftime(fmt).to_string(index=False))


if __name__ == "__main__":
    run_code()
