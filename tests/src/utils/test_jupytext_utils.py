import os.path

import pytest

from src.utils.jupytext_utils import generated_by_jupytext

@pytest.mark.parametrize(
    "file_path, result_expected",
    [
        ('src/notebooks/get ticker info.py', True),
        ('src/utils/date_utils.py', False)
    ]
)
def test_generated_by_jupytext(file_path, result_expected):
    this_file = os.path.abspath(__file__)
    this_dir = os.path.dirname(this_file)
    project_dir = os.path.dirname(os.path.dirname(os.path.dirname(this_dir)))
    file_path = os.path.join(project_dir, file_path)
    result_got = generated_by_jupytext(file_path)
    assert result_got == result_expected, "For {}, expecting {} but got {}".format(file_path, result_expected, result_got)
