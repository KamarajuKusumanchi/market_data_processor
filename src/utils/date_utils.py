from datetime import datetime, timedelta


def diff_yyyymmdd(dt1: str, dt2: str) -> int:
    # Get the number of days between two dates given in YYYYMMDD format
    # tags | diff_days
    date1 = datetime.strptime(dt1, "%Y%m%d")
    date2 = datetime.strptime(dt2, "%Y%m%d")
    diff_days = (date2 - date1).days
    return diff_days


def previous_month_end(dt_yyyymmdd: str) -> str:
    # Given a date in YYYYMMDD form, get the date of previous month end in YYYYMMDD form.
    # For example
    #   input,    output
    #   20230801, 20230731
    #   20230815, 20230731
    #   20230831, 20230731
    #   20230901, 20230831
    #   20240102, 20231231
    # If you want to set dt_yyyymmdd to the current date, use
    #   from datetime import date
    #   today = date.today().strftime('%Y%m%d')
    dt = datetime.strptime(dt_yyyymmdd, "%Y%m%d").date()
    first = dt.replace(day=1)
    last_month_end = first - timedelta(days=1)
    last_month_end = last_month_end.strftime("%Y%m%d")
    return last_month_end
