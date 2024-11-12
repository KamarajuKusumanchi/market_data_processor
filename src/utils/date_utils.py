from datetime import datetime, timedelta, date


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
    # tags | last month end
    dt = datetime.strptime(dt_yyyymmdd, "%Y%m%d").date()
    first = dt.replace(day=1)
    last_month_end = first - timedelta(days=1)
    last_month_end = last_month_end.strftime("%Y%m%d")
    return last_month_end


def third_friday(year: int, month: int) -> str:
    """
    Return the third Friday for a given year and month.
    For example:
      year, month, output
      2024, 1, 20240119
      2024, 2, 20240216
      2024, 3, 20240315
    More data can be seen at https://www.marketwatch.com/tools/options-expiration-calendar?year=2024
    Use case:
      Equity options expire on third Friday of each month.

    Initial version of the code is from https://stackoverflow.com/a/47931869/6305733
    """
    # The 15th is the lowest third day in the month
    third = date(year, month, 15)
    # What day of the week is the 15th?
    w = third.weekday()
    # Per https://docs.python.org/3/library/datetime.html#datetime.date.weekday
    # weekday returns the day of the week as an integer, where Monday is 0 and Sunday is 6.
    # So, Friday is weekday 4
    if w != 4:
        # Replace just the day (of month)
        third = third.replace(day=(15 + (4 - w) % 7))
    third = third.strftime("%Y%m%d")
    return third
