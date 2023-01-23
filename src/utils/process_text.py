import re


def words(text):
    # Initial version is from https://norvig.com/spell-correct.html
    return re.findall(r"\w+", text.lower())
