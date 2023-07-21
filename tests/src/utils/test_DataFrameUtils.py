import numpy as np
import pandas as pd
import pytest

from src.utils.DataFrameUtils import to_fwf, lookup_latest


def test_to_fwf_with_index(tmpdir):
    df = pd.DataFrame(np.linspace(0, 1, 9).reshape(3, 3))
    # The tmpdir fixture is explained in https://docs.pytest.org/en/6.2.x/tmpdir.html
    file = tmpdir.join("with_index.txt")
    df.to_fwf(file, index=True)
    contents_expected = (
        "        0      1      2\n"
        " 0  0      0.125  0.25\n"
        " 1  0.375  0.5    0.625\n"
        " 2  0.75   0.875  1\n"
    )
    contents_got = file.read()
    assert contents_got == contents_expected


def test_to_fwf_no_index(tmpdir):
    df = pd.DataFrame(np.linspace(0, 1, 9).reshape(3, 3))
    # The tmpdir fixture is explained in https://docs.pytest.org/en/6.2.x/tmpdir.html
    file = tmpdir.join("no_index.txt")
    df.to_fwf(file, index=False)
    contents_expected = (
        "    0      1      2\n"
        "0      0.125  0.25\n"
        "0.375  0.5    0.625\n"
        "0.75   0.875  1\n"
    )
    contents_got = file.read()
    assert contents_got == contents_expected

@pytest.mark.parametrize(
    "doi, y_expected",
    [
        ('2021-05-01', np.nan),
        ('2022-01-01', 200),
        ('2022-05-01', 200),
        ('2023-01-01', 100),
        ('2023-05-01', 100),
        ('2024-01-01', 300),
        ('2024-05-01', 300),
    ],
)
def test_lookup_latest(doi, y_expected):
    # Features of the dataset:
    # * The dates are not in chronological order
    # * A date might occur in multiple rows (in which case, we should pick the latest.
    df = pd.DataFrame(
        [['2023-01-01', 500],
         ['2022-01-01', 200],
         ['2024-01-01', 300],
         ['2023-01-01', 100],
         ],
    columns = ['date', 'y'])
    got = lookup_latest(doi, df, 'date', 'y')

    if pd.isna(y_expected):
        assert pd.isna(got), "Expecting {} but got {}".format(y_expected, got)
    else:
        assert got == y_expected, "Expecting {} but got {}".format(y_expected, got)
