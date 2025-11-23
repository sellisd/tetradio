# src/test_tools.py

import pytest
from tools import text_normalize

@pytest.mark.parametrize(
    "input_text,expected",
    [
        # Simple ASCII
        ("Hello World", "hello world"),
        # Lowercasing
        ("HELLO world", "hello world"),
        # Unicode normalization (NFKC): full-width to ASCII
        ("ＡＢＣ１２３", "abc123"),
        # Accented characters (should remain, but normalized)
        ("Café", "café"),
        # Remove punctuation
        ("Hello, world!", "hello world"),
        ("Good morning: everyone.", "good morning everyone"),
        # Remove special characters
        ("Hello @world #2024!", "hello world 2024"),
        # Whitespace normalization
        ("Hello   world", "hello world"),
        ("Hello\tworld", "hello world"),
        ("Hello\nworld", "hello world"),
        ("Hello \n\t world", "hello world"),
        # Leading/trailing whitespace
        ("   Hello world   ", "hello world"),
        ("\n\tHello world\t\n", "hello world"),
        # Combination of all
        ("  Héllo,   Wörld! \n\t", "héllo wörld"),
        ("  \tNúmbérs: １２３, symbols!@#\n", "númbérs 123 symbols"),
        # Only special characters (should become empty)
        ("!@#$%^&*()", ""),
        # Only whitespace (should become empty)
        ("   \n\t  ", ""),
    ]
)
def test_text_normalize(input_text, expected):
    assert text_normalize(input_text) == expected