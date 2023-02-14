import numpy as np
import pandas as pd

from src.utils.DataFrameUtils import to_fwf


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
