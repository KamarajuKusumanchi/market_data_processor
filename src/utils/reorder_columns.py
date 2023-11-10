#! /usr/bin/env python
import argparse
import csv
import re
import sys

def reorder_columns(infile, outfile, new_fields):
    # Todo:
    # * Add a test case for this.
    # * Support the case where input is from stdin and output is to stdout (instead of files).
    # reorder columns in a csv file
    # reads from infile and writes to outfile.
    #
    # Assumptions:
    # * comments are assumed to span over the entire line.
    # * inline comments (ex:- 1,2,3 #comment here) are not supported.
    #
    # Requirements:
    # * Any comments or empty lines should be preserved asis
    #
    # Close but no cigar:
    # * https://stackoverflow.com/questions/33001490/python-re-ordering-columns-in-a-csv
    #   solves the same problem but the solution does not handle the case
    #   where the csv file contains comments.
    empty_pattern = r"^\s*$"
    comment_pattern = r"^\s*#"

    # find the fields
    reader = csv.reader(infile, quoting=csv.QUOTE_NONE)
    for row in reader:
        if not row:
            # If the input is a pure empty line (r"^$"), then row is an
            # empty list. In that case, we can't do row[0] as it will throw
            #   IndexError: list index out of range
            # error
            continue
        else:
            first_element = row[0]
        if re.search(comment_pattern, first_element):
            continue
        elif re.search(empty_pattern, first_element):
            continue
        else:
            fields = row
            break
    # print(fields)
    new_field_index = [fields.index(i) for i in new_fields]

    infile.seek(0)
    reader = csv.reader(infile, quoting=csv.QUOTE_NONE)
    for row in reader:
        if not row:
            outfile.write("\n")
            continue
        else:
            first_element = row[0]
        if re.search(comment_pattern, first_element):
            outfile.write(",".join(row) + "\n")
        elif re.search(empty_pattern, first_element):
            outfile.write(",".join(row) + "\n")
        else:
            new_row = [row[i] for i in new_field_index]
            outfile.write(",".join(new_row) + "\n")

def create_parser():
    parser = argparse.ArgumentParser(
        description="Reorder columns in a csv file while preserving comments and empty lines."
    )
    # Per https://bugs.python.org/issue24739 argparse.FileType does not allow newline argument.
    # So we can't do something like
    #     parser.add_argument(
    #         '-i', '--input', dest="input_file", type=argparse.FileType('r', newline=''),
    #         default=sys.stdin, help='input file')
    # and
    #     parser.add_argument(
    #         '-o', '--output', dest='output_file', type=argparse.FileType('w', newline=''),
    #         default=sys.stdout, help='output file')
    # So accept the file path as argument
    parser.add_argument(
        '-i', '--input-file', dest="input_file",
        default=None, help='input file')
    parser.add_argument(
        '-o', '--output-file', dest='output_file',
        default=None, help='output file')
    parser.add_argument(
        '-c', '--columns', dest="columns", nargs='+',
        help="list of columns separated by spaces", required=True)
    return parser

if __name__ == '__main__':
    input_file_path = '../../tests/src/utils/reorder_columns_data/input.csv'
    output_file_path = '../../tests/src/utils/reorder_columns_data/output_expected.csv'
    new_fields = ['A', 'C', 'D', 'E', 'B']
    with open(input_file_path, newline='') as infile, \
        open(output_file_path, 'w', newline='') as outfile:
        reorder_columns(infile, outfile, new_fields)

    # Todo: Currently, the reorder_columns() does two passes.
    #  One pass to find the fields and another pass to rearrange the columns.
    #  This will not work if the input is sys.stdin since we can't do seek(0) on sys.stdin.
    #  Afterwards, improve the algorithm to do everything in one pass.
    #
    # parser = create_parser()
    # args = parser.parse_args()
    # input_file_path = args.input_file
    # output_file_path = args.output_file
    # new_fields = args.columns
    #
    # if input_file_path:
    #     infile = open(input_file_path, newline='')
    # else:
    #     infile = sys.stdin
    # if output_file_path:
    #     outfile = open(output_file_path, 'w', newline='')
    # else:
    #     outfile = sys.stdout
    #
    # reorder_columns(infile, outfile, new_fields)
    #
    # if infile is not sys.stdin:
    #     infile.close()
    # if outfile is not sys.stdout:
    #     outfile.close()
