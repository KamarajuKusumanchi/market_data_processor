import os
import pandas as pd

from tabulate import tabulate


def to_fwf(df, fname, index=True):
    # Initial version is from https://stackoverflow.com/a/35974742
    fname = os.path.expanduser(fname)
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
    with open(fname, "w") as FileObj:
        FileObj.write(content)


pd.DataFrame.to_fwf = to_fwf
