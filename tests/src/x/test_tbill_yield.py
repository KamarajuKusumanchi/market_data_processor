import pytest
from src.x.tbill_yield import tbill_yield


@pytest.mark.parametrize(
    "P, r, yield_expected", [(99.93778, 28, 0.814), (99.5905, 28, 5.375)]
)
def test_tbill_yield(P, r, yield_expected):
    yield_got = tbill_yield(P, r)
    assert (
        yield_got == yield_expected
    ), "For P = {}, r = {}, yield_got = {}, yield_expected = {}".format(
        P, r, yield_got, yield_expected
    )


def test_tbill_yield_long_maturity():
    P = 99.5905
    r = 183
    with pytest.raises(AssertionError):
        tbill_yield(P, r)
