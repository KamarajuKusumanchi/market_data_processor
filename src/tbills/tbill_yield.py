def tbill_yield(P, r, y):
    # Compute the yield of a tbill
    # P = price
    # r = days to maturity
    # y = days in year
    b = r / y
    if b <= 0.5:
        i = tbill_yield_short_maturity(P, r, y)
    else:
        i = tbill_yield_long_maturity(P, r, y)
    return i


def tbill_yield_short_maturity(P, r, y):
    # Calculate "Coupon Equivalent Yield" for bills of not more than one
    # half-year to maturity
    # P = price
    # r = days to maturity
    # y = days in year
    # Ref:- Example in pg-2 of https://www.treasurydirect.gov/instit/annceresult/press/preanre/2004/ofcalc6decbill.pdf
    assert (
        r < 0.5 * y
    ), f"Invalid inputs: r = {r}, y = {y}. Bills should not have more than one half-year to maturity."
    i = ((100 - P) / P) * (y / r)
    i = round(i * 100, 3)
    return i


def tbill_yield_long_maturity(P, r, y):
    # Calculate "Coupon Equivalent Yield" for bills of more than one half-year
    # to maturity
    # P = price
    # r = days to maturity
    # y = days in year
    # Ref:- Example in pg-2 of https://www.treasurydirect.gov/instit/annceresult/press/preanre/2004/ofcalc6decbill.pdf
    assert (
        r > 0.5 * y
    ), f"Invalid inputs: r = {r}, y = {y}. Bills should have more than one half-year to maturity."
    b = r / y
    a = (r / (2 * y)) - 0.25
    c = (P - 100) / P
    discriminant = b**2 - 4 * a * c
    i = (-b + discriminant**0.5) / (2 * a)
    i = round(i * 100, 3)
    return i


def tax_equivalent_treasury_yield(t, f, s):
    # Let's say, t is the yield of a Treasury, f is the federal tax rate,
    # and s is the state tax rate. Then, the tax-equivalent yield of a Treasury
    # would be  t * (1-f) / (1-f-s)
    # Ref:- https://thefinancebuff.com/brokered-cd-vs-direct-cd-vs-treasury-worth-it.html
    # For example, for a Treasury yield of 4.95%, federal tax rate of 22%,
    # state tax rate of 6%, the tax equivalent Treasury yield would be
    # 4.95 * (1-0.22) / (1-0.22-0.06) = 5.363%
    #
    # Sample inputs: (t, f, s) = (4.95, 22, 6)
    # Sample output: 5.363
    f /= 100
    s /= 100
    te = t * (1 - f) / (1 - f - s)
    te = round(te, 3)
    return te


if __name__ == "__main__":
    i = tbill_yield(99.5905, 183, 366)
    print(i)
