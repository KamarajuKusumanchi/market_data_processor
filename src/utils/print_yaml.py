#! /usr/bin/env python
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
    # Using the tip from https://stackoverflow.com/questions/7576525/optional-stdin-in-python-with-argparse
    parser.add_argument("file_name", nargs='?', type=argparse.FileType('r'),
                        action="store", help="file name", default=sys.stdin)
    return parser


def read_yaml(file_name):
    data = yaml.load(file_name)
    return data


if __name__ == "__main__":
    run_code()
