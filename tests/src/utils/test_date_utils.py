from src.utils.date_utils import diff_yyyymmdd


def test_diff_yyyymmdd():
    dt1 = "20221031"
    dt2 = "20221230"
    days_got = diff_yyyymmdd(dt1, dt2)
    days_expected = 60
    assert days_got == days_expected
