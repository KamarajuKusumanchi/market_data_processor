import pytest
from src.tbills.tbill_yield import (
    tbill_yield,
    tbill_yield_short_maturity,
    tbill_yield_long_maturity,
    tax_equivalent_treasury_yield,
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


def test_tax_equivalent_treasury_yield():
    (t, f, s) = (4.95, 22, 6)
    te_got = 5.363
    te_expected = tax_equivalent_treasury_yield(t, f, s)
    assert te_got == te_expected, (
        f"Tax equivalent Treasury yield calculation is broken. "
        f"For (t, f, s) = ({t}, {f}, {s}), te_got = {te_got}, "
        f"te_expected = {te_expected}"
    )
