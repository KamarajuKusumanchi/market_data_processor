import project_root
from src.market_cap.get_market_cap import get_market_cap
from src.market_cap.get_nasdaq_data import get_nasdaq_data, convert_nasdaq_data_to_df


def test_get_market_cap():
    nasdaq_data = get_nasdaq_data()
    nasdaq_df = convert_nasdaq_data_to_df(nasdaq_data)
    limit = 10
    market_cap = get_market_cap(nasdaq_df, limit)
    shape_expected = (limit, 3)
    shape_got = market_cap.shape
    assert shape_got == shape_expected, "Expecting {} but got {}".format(
        shape_expected, shape_got
    )
