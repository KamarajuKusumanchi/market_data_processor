# Add sp500 tickers to the universe
# Sample usage:
# $python ./add_sp500_tickers_to_univ.py > ../market_data/universe/new_univ
# cd ../market_data/universe
# vimdiff univ new_univ

import pandas as pd
import sys

from src.scripts.sp500_tickers import get_sp500_table


def add_sp500_tickers(univ):
    univ_id = univ.columns[0]
    wiki_id = 'Symbol'
    sp500 = get_sp500_table(wiki_id).rename({wiki_id: univ_id}, axis=1)
    new_univ = pd.concat((univ, sp500), ignore_index=True, sort=True)\
        .sort_values(by=univ_id)\
        .drop_duplicates()
    return new_univ


if __name__ == '__main__':
    univ = pd.read_csv('../market_data/universe/univ')
    new_univ = add_sp500_tickers(univ)
    new_univ.to_csv(sys.stdout, index=False)
