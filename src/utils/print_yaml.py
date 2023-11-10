#! /usr/bin/env python
# Utility script to print an yaml file on the command line.
# Usage:
# <script_name> file.yaml
# <script_name> < file.yaml
#
# Sample run:
# $ ./print_yaml.py ../../../company_description/word_groups.yaml
# - [grocery, groceries]
#
# $ ./print_yaml.py < ../../../company_description/word_groups.yaml
# - [grocery, groceries]

import argparse
import ruamel.yaml
import sys

# Using the new syntax from https://yaml.readthedocs.io/en/latest/api.html
yaml = ruamel.yaml.YAML(typ="safe", pure=True)


def run_code():
    parser = create_parser()
    args = parser.parse_args()
    # Note:- file_name is of type _io.TextIOWrapper, not str
    file_name = args.file_name
    # print(type(file_name))
    data = read_yaml(file_name)
    yaml.dump(data, sys.stdout)


def create_parser():
    parser = argparse.ArgumentParser(
        description="Read and write a yaml file using using python."
    )
    # Using the tip from https://stackoverflow.com/questions/7576525/optional-stdin-in-python-with-argparse
    parser.add_argument("file_name", nargs='?', type=argparse.FileType('r'),
                        action="store", help="file name", default=sys.stdin)
    return parser


def read_yaml(stream):
    data = yaml.load(stream)
    return data


if __name__ == "__main__":
    run_code()
