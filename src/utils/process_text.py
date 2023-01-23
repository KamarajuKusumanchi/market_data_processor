import re


def words(text):
    return re.findall(r"\w+", text.lower())
