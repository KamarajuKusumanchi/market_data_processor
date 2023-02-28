import os
import pandas as pd
import sys

from tabulate import tabulate


def to_fwf(df, fname_or_stdout, index=True):
    # Initial version is from https://stackoverflow.com/a/35974742
    #
    # Note: I want to keep the interface same as pandas.DataFrame.to_csv for
    # as much as possible. That is why 'index' is a boolean variable with
    # default True.
    # Ref:- https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_csv.html
    if index:
        show_index = list(df.index)
    else:
        show_index = False
    content = tabulate(
        df.values.tolist(), list(df.columns), showindex=show_index, tablefmt="plain"
    )
    # The above generates strings such as
    # '...\n...\n...\n...'
    # Add a new line character at the end to make the output work nicely with the cat command.
    content += "\n"

    if isinstance(fname_or_stdout, str):
        write_to_file = True
        fname = os.path.expanduser(fname_or_stdout)
        FileObj = open(fname, "w")
    else:
        # We are probably writing to sys.stdout
        write_to_file = False
        FileObj = fname_or_stdout

    FileObj.write(content)

    if write_to_file:
        FileObj.close()


pd.DataFrame.to_fwf = to_fwf
