def tbill_yield(P, r):
    # Compute the yield of a tbill that will mature in not more than one half-year.
    # P = price
    # r = days to maturity
    y = 366
    assert (
        r < 0.5 * 366
    ), "logic not implemented for securities maturing in more than one half-year."
    i = ((100 - P) / P) * (y / r)
    i = round(i * 100, 3)
    return i


if __name__ == "__main__":
    i = tbill_yield(99.5905, 183)
    print(i)
