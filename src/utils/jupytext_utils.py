from jupytext.header import header_to_metadata_and_cell

def generated_by_jupytext(file_path):
    # Check if a given python script is generated by jupytext or not.
    # Mimicing the approach used in
    # https://github.com/mwouts/jupytext/blob/main/src/jupytext/formats.py -> divine_format()
    # To experiment, see "src/notebooks/generated by jupytext.ipynb"
    with open(file_path) as fp:
        text = fp.read()
    lines = text.splitlines()
    comment = "#"
    metadata, _, _, _ = header_to_metadata_and_cell(lines, comment, "")
    result = 'jupytext' in metadata.keys()
    return result
