#! /usr/bin/env python

import sys
from datetime import datetime, timedelta
import argparse

# Script to add a given number of weeks to a date.

# Todo:-
# (1) Extend the script to any number of arguments. For example,
# script_name <dt> offset1 offset2 offset3 ...

def parse_arguments(args):
    parser = argparse.ArgumentParser(
        description='Add a given number of weeks to a date.',
        formatter_class = argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "dt", action='store',
        help='date'
    )
    parser.add_argument(
        "offset", action='store',
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

    dt = args.dt
    offset = int(args.offset)
    if len(dt) == 8:
        fmt = '%Y%m%d'
    elif len(dt) == 10:
        fmt = '%Y-%m-%d'
    else:
        print('date = ', dt, ' is in unrecognizable format.')
        sys.exit(1)

    new_dt = datetime.strptime(dt, fmt) + timedelta(weeks=offset)
    print(new_dt.strftime(fmt))


if __name__ == "__main__":
    run_code()
