import pytest
import pandas as pd
from pandas.testing import assert_frame_equal
from src.utils.dokuwiki_parser import parse_dokuwiki_table

# changelog:
# * 2026-05-18: initial version is from @claude.


@pytest.fixture
def simple_table():
    return """
^ Name      ^ Age ^ City      ^
| Alice     | 30  | New York  |
| Bob       | 25  | London    |
| Charlie   | 35  | Tokyo     |
"""


def test_simple_table(simple_table):
    expected = pd.DataFrame(
        {
            "Name": ["Alice", "Bob", "Charlie"],
            "Age": ["30", "25", "35"],
            "City": ["New York", "London", "Tokyo"],
        }
    )
    assert_frame_equal(parse_dokuwiki_table(simple_table), expected)


@pytest.fixture
def no_header_table():
    return """
| Alice | 30 | New York |
| Bob   | 25 | London   |
"""


def test_no_header_table(no_header_table):
    expected = pd.DataFrame(
        [
            ["Alice", "30", "New York"],
            ["Bob", "25", "London"],
        ]
    )
    assert_frame_equal(parse_dokuwiki_table(no_header_table), expected)


@pytest.fixture
def single_row_table():
    return """
^ Name ^ Age ^
| Alice | 30 |
"""


def test_single_row_table(single_row_table):
    expected = pd.DataFrame({"Name": ["Alice"], "Age": ["30"]})
    assert_frame_equal(parse_dokuwiki_table(single_row_table), expected)


@pytest.fixture
def single_column_table():
    return """
^ Name ^
| Alice |
| Bob   |
"""


def test_single_column_table(single_column_table):
    expected = pd.DataFrame({"Name": ["Alice", "Bob"]})
    assert_frame_equal(parse_dokuwiki_table(single_column_table), expected)


@pytest.fixture
def whitespace_table():
    return """
^   Name   ^   Age   ^
|   Alice  |   30    |
|   Bob    |   25    |
"""


def test_whitespace_table(whitespace_table):
    expected = pd.DataFrame({"Name": ["Alice", "Bob"], "Age": ["30", "25"]})
    assert_frame_equal(parse_dokuwiki_table(whitespace_table), expected)


def test_empty_string_returns_empty_dataframe():
    assert_frame_equal(parse_dokuwiki_table(""), pd.DataFrame())


def test_header_only_no_data_rows():
    expected = pd.DataFrame(columns=["Name", "Age", "City"])
    assert_frame_equal(parse_dokuwiki_table("^ Name ^ Age ^ City ^"), expected)
