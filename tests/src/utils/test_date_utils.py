import pytest

from src.utils.date_utils import diff_yyyymmdd, previous_month_end, third_friday


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


@pytest.mark.parametrize(
    "year, month, third_friday_expected",
    [
        (2024, 1, "20240119"),
        (2024, 2, "20240216"),
        (2024, 3, "20240315"),
        (2024, 4, "20240419"),
        (2024, 5, "20240517"),
        (2024, 6, "20240621"),
        (2024, 7, "20240719"),
        (2024, 8, "20240816"),
        (2024, 9, "20240920"),
        (2024, 10, "20241018"),
        (2024, 11, "20241115"),
        (2024, 12, "20241220"),

    ],
)
def test_third_friday(year, month, third_friday_expected):
    # Used https://www.marketwatch.com/tools/options-expiration-calendar?year=2024 to get the data for the test cases
    third_friday_got = third_friday(year, month)
    assert third_friday_got == third_friday_expected, "Expecting {} but got {}".format(
        third_friday_expected, third_friday_got
    )
