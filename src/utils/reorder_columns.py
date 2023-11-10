import csv
import re
import sys

def reorder_columns(infile, outfile, new_fields):
    # Todo:
    # * Add a test case for this.
    # * Support the case where input is from stdin and output is to stdout (instead of files).
    # reorder columns in a csv file
    # reads from infile_path and writes to outfile_path.
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

if __name__ == '__main__':
    infile_path = '../../tests/src/utils/csv_utils_data/input.csv'
    outfile_path = '../../tests/src/utils/csv_utils_data/output_expected.csv'
    new_fields = ['A', 'C', 'D', 'E', 'B']
    with open(infile_path, newline='') as infile, \
        open(outfile_path, 'w', newline='') as outfile:
        reorder_columns(infile, outfile, new_fields)
    if infile is not sys.stdin:
        infile.close()
    if outfile is not sys.stdout:
        outfile.close()
