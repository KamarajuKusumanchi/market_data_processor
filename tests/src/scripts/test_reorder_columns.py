import os.path
from io import StringIO

from src.scripts.reorder_columns import reorder_columns


def test_reorder_columns():
    this_file = os.path.abspath(__file__)
    this_dir = os.path.dirname(this_file)
    data_dir = os.path.join(this_dir, 'reorder_columns_data')

    input_file_path = os.path.join(data_dir, 'input.csv')
    infile = open(input_file_path, newline='')
    outfile = StringIO()
    new_fields = ['A', 'C', 'D', 'E', 'B']

    reorder_columns(infile, outfile, new_fields)
    output_got = outfile.getvalue().splitlines()
    infile.close()
    outfile.close()

    output_expected_file_path = os.path.join(data_dir, 'output_expected.csv')
    output_expected_file = open(output_expected_file_path, newline='')
    output_expected = output_expected_file.read().splitlines()
    output_expected_file.close()

    assert output_got == output_expected, 'Got unexpected output'
