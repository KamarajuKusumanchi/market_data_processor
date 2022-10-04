#! /usr/bin/env python
# Utility script to print an yaml file on the command line.
# Usage:
# <script_name> file.yaml
#
# Sample run:
# ./print_yaml_v1.py ../../../company_description/word_groups.yaml
# - [grocery, groceries]
#
# Limitations:
#  * It can't handle input from stdin. For example, we can't do
#      <script_name> < file.yaml
#
#      $ ./print_yaml_v1.py < ../../../company_description/word_groups.yaml
#      usage: print_yaml_v1.py [-h] file_name
#      print_yaml_v1.py: error: the following arguments are required: file_name
#  This is fixed in latter versions of the script, print_yaml.py, but
#  I am keeping this for reference.

import argparse
import ruamel.yaml
import sys

# Using the new syntax from https://yaml.readthedocs.io/en/latest/api.html
yaml = ruamel.yaml.YAML(typ="safe", pure=True)


def run_code():
    parser = parse_arguments()
    args = parser.parse_args()
    file_name = args.file_name
    data = read_yaml(file_name)
    yaml.dump(data, sys.stdout)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Read and write a yaml file using using python."
    )
    parser.add_argument("file_name", action="store", help="file name")
    return parser


def read_yaml(file_name):
    # Using sample code from https://stackoverflow.com/a/38922434/6305733
    with open(file_name) as stream:
        data = yaml.load(stream)
    return data


if __name__ == "__main__":
    run_code()
