import pytest
from chunker import split_paragraphs_sliding_window

def test_split_paragraphs_sliding_window_basic():
    text = "Para1.\n\nPara2.\n\nPara3.\n\nPara4."
    result = split_paragraphs_sliding_window(text, window_size=2, min_chunk_length=0)
    expected = [
        "Para1.\n\nPara2.",
        "Para2.\n\nPara3.",
        "Para3.\n\nPara4.",
        "Para4."
    ]
    assert result == expected

def test_split_paragraphs_sliding_window_window_size_3():
    text = "A\n\nB\n\nC\n\nD"
    result = split_paragraphs_sliding_window(text, window_size=3, min_chunk_length=0)
    expected = [
        "A\n\nB\n\nC",
        "B\n\nC\n\nD",
        "C\n\nD",
        "D"
    ]
    assert result == expected

def test_split_paragraphs_sliding_window_too_few_paragraphs():
    text = "Only one paragraph."
    result = split_paragraphs_sliding_window(text, window_size=2, min_chunk_length=0)
    # With only one paragraph and window_size=2, no chunk can be formed
    assert result == ["Only one paragraph."]

def test_split_paragraphs_sliding_window_exact_window():
    text = "P1\n\nP2"
    result = split_paragraphs_sliding_window(text, window_size=2, min_chunk_length=0)
    expected = ["P1\n\nP2", "P2"]
    assert result == expected

def test_split_paragraphs_sliding_window_ignores_empty():
    text = "A\n\n\n\nB\n\n   \n\nC"
    result = split_paragraphs_sliding_window(text, window_size=2, min_chunk_length=0)
    expected = [
        "A\n\nB",
        "B\n\nC",
        "C"
    ]
    assert result == expected

def test_split_paragraphs_sliding_window_min_chunk_length():
    text = "A.\n\nB.\n\nC.\n\nD."
    # Each paragraph is 2 chars, window_size=2, min_chunk_length=6
    result = split_paragraphs_sliding_window(text, window_size=2, min_chunk_length=6)
    # The function will append paragraphs until the chunk is >= 6 chars
    expected = [
        "A.\n\nB.",
        "B.\n\nC.",
        "C.\n\nD.",
        "D."
    ]
    assert result == expected