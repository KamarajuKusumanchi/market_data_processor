#! /usr/bin/env python
import argparse
import csv
import re
import sys

def reorder_columns(infile, outfile, new_fields):
    # Todo:
    # * Add a test case for this.
    # reorder columns in a csv file
    # reads from infile and writes to outfile.
    #
    # Assumptions:
    # * comments are assumed to span over the entire line.
    # * inline comments (ex:- 1,2,3 #comment here) are not supported.
    #
    # Requirements:
    # * infile can be sys.stdin or a file object.
    # * outfile can be sys.stdout or a file object.
    # * Any comments or empty lines should be preserved asis
    # * input should be read only once and processed in one pass.
    #   For example, we can't do one pass to find the fields and another pass
    #   to rearrange them. That would not work if the input is sys.stdin as we
    #   can't do seek(0) on it.
    #
    # Close but no cigar:
    # * https://stackoverflow.com/questions/33001490/python-re-ordering-columns-in-a-csv
    #   solves the same problem but the solution does not handle the case
    #   where the csv file contains comments.
    empty_pattern = r"^\s*$"
    comment_pattern = r"^\s*#"
    header_not_found = True
    reader = csv.reader(infile, quoting=csv.QUOTE_NONE)
    for row in reader:
        if not row:
            # If the input is a pure empty line (r"^$"), then row is an
            # empty list. In that case, we can't do row[0] as it will throw
            #   IndexError: list index out of range
            # error. So write an empty line and continue.
            outfile.write("\n")
            continue
        else:
            first_element = row[0]
        if re.search(comment_pattern, first_element):
            outfile.write(",".join(row) + "\n")
        elif re.search(empty_pattern, first_element):
            outfile.write(",".join(row) + "\n")
        else:
            if header_not_found:
                header_not_found = False
                fields = row
                # print(fields)
                new_field_index = [fields.index(i) for i in new_fields]
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
    # So accept the file path as argument and create file objects yourself.
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
    # input_file_path = '../../tests/src/scripts/reorder_columns_data/input.csv'
    # output_file_path = '../../tests/src/scripts/reorder_columns_data/output_expected.csv'
    # new_fields = ['A', 'C', 'D', 'E', 'B']

    parser = create_parser()
    args = parser.parse_args()
    input_file_path = args.input_file
    output_file_path = args.output_file
    new_fields = args.columns

    # with open(input_file_path, newline='') as infile, \
    #     open(output_file_path, 'w', newline='') as outfile:
    #     reorder_columns(infile, outfile, new_fields)

    if input_file_path:
        infile = open(input_file_path, newline='')
    else:
        infile = sys.stdin
    if output_file_path:
        outfile = open(output_file_path, 'w', newline='')
    else:
        outfile = sys.stdout

    reorder_columns(infile, outfile, new_fields)

    if infile is not sys.stdin:
        infile.close()
    if outfile is not sys.stdout:
        outfile.close()
