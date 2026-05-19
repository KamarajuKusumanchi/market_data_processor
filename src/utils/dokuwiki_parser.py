import pandas as pd
import re

# changelog:
# * 2026-05-18: initial version is from @claude.


def parse_dokuwiki_table(table_str: str) -> pd.DataFrame:
    # Sample usage:
    # table = """
    # ^ Name    ^ Age ^ City     ^
    # | Alice   | 30  | New York |
    # | Bob     | 25  | London   |
    # | Charlie | 35  | Tokyo    |
    # """
    #
    # df = parse_dokuwiki_table(table)
    # print(df)
    #
    # To read from a file:
    # with open("my_table.txt", "r", encoding="utf-8") as f:
    #     content = f.read()
    #
    # df = parse_dokuwiki_table(content)

    headers = []
    rows = []

    for line in table_str.strip().splitlines():
        line = line.strip()
        if not line:
            continue

        # Header rows start and end with ^
        if line.startswith("^"):
            cells = [c.strip() for c in re.split(r'\^', line) if c.strip()]
            headers = cells

        # Data rows start and end with |
        elif line.startswith("|"):
            cells = [c.strip() for c in re.split(r'\|', line) if c.strip()]
            rows.append(cells)

    df = pd.DataFrame(rows, columns=headers if headers else None)
    return df
