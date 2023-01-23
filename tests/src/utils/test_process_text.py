import pytest
from src.utils.process_text import words


@pytest.mark.parametrize(
    "text, words_expected",
    [
        ("foo bar", ["foo", "bar"]),
        ("foo", ["foo"]),
        ("", []),
        ("Foo Bar", ["foo", "bar"]),
    ],
)
def test_words(text, words_expected):
    words_got = words(text)
    assert words_got == words_expected, "Expecting {} but got {}".format(
        words_expected, words_got
    )
