import pytest

from src.utils.date_utils import diff_yyyymmdd, previous_month_end


def test_diff_yyyymmdd():
    dt1 = "20221031"
    dt2 = "20221230"
    days_got = diff_yyyymmdd(dt1, dt2)
    days_expected = 60
    assert days_got == days_expected


@pytest.mark.parametrize(
    "input_date, output_date_expected",
    [
        ("20230801", "20230731"),
        ("20230815", "20230731"),
        ("20230831", "20230731"),
        ("20230901", "20230831"),
        ("20240102", "20231231"),
    ],
)
def test_previous_month_end(input_date, output_date_expected):
    output_date_got = previous_month_end(input_date)
    assert output_date_got == output_date_expected, "Expecting {} but got {}".format(
        output_date_expected, output_date_got
    )
