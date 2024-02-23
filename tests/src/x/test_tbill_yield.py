import pytest
from src.x.tbill_yield import (
    tbill_yield,
    tbill_yield_short_maturity,
    tbill_yield_long_maturity,
)


@pytest.mark.parametrize(
    "P, r, y, yield_expected",
    [
        (99.93778, 28, 366, 0.814),
        (99.5905, 28, 366, 5.375),
        (95.252833, 364, 366, 4.950),
    ],
)
def test_tbill_yield(P, r, y, yield_expected):
    yield_got = tbill_yield(P, r, y)
    assert (
        yield_got == yield_expected
    ), "For P = {}, r = {}, y = {}, yield_got = {}, yield_expected = {}".format(
        P, r, y, yield_got, yield_expected
    )


@pytest.mark.parametrize(
    "P, r, y, yield_expected",
    [
        (99.93778, 28, 366, 0.814),
        (99.5905, 28, 366, 5.375),
    ],
)
def test_tbill_yield_short_maturity(P, r, y, yield_expected):
    yield_got = tbill_yield(P, r, y)
    assert (
        yield_got == yield_expected
    ), "For P = {}, r = {}, y = {}, yield_got = {}, yield_expected = {}".format(
        P, r, y, yield_got, yield_expected
    )


def test_tbill_yield_short_maturity_with_long_maturity():
    (P, r, y) = (95.5905, 183, 366)
    # Using the example listed in https://docs.pytest.org/en/latest/how-to/assert.html to catch the AssertionError.
    with pytest.raises(AssertionError):
        tbill_yield_short_maturity(P, r, y)


@pytest.mark.parametrize(
    "P, r, y, yield_expected",
    [
        (95.252833, 364, 366, 4.950),
    ],
)
def test_tbill_yield_long_maturity(P, r, y, yield_expected):
    yield_got = tbill_yield(P, r, y)
    assert (
        yield_got == yield_expected
    ), "For P = {}, r = {}, y = {}, yield_got = {}, yield_expected = {}".format(
        P, r, y, yield_got, yield_expected
    )


def test_tbill_yield_long_maturity_with_short_maturity():
    (P, r, y) = (99.5905, 28, 366)
    # Using the example listed in https://docs.pytest.org/en/latest/how-to/assert.html to catch the AssertionError.
    with pytest.raises(AssertionError):
        tbill_yield_long_maturity(P, r, y)
