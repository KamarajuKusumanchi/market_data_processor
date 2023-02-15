import pandas as pd
from datetime import datetime


def diff_yyyymmdd(dt1: str, dt2: str) -> int:
    # Get the number of days between two dates given in YYYYMMDD format
    # tags | diff_days
    date1 = datetime.strptime(dt1, "%Y%m%d")
    date2 = datetime.strptime(dt2, "%Y%m%d")
    diff_days = (date2 - date1).days
    return diff_days
