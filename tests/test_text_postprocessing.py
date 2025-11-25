import pytest
from extractor import Extractor

import pytest

@pytest.fixture
def extractor():
    return Extractor(source="She always helps me. It was a sunny day. We play soccer together. It looks comfortable. She loves the outdoors. They always support each other. They are close.")

def test_valid_relationship_and_quoted_text(extractor):
    text = "Alice is Bob's sister. \"She always helps me.\""
    result = extractor.postprocess_text_spacy(text)
    assert result == [("Alice", "Bob", "sister", '"She always helps me."')]

def test_no_relationship(extractor):
    text = "Alice went to the park. \"It was a sunny day.\""
    result = extractor.postprocess_text_spacy(text)
    assert result == []

def test_multiple_lines_with_relationships(extractor):
    text = (
        "Alice is Bob's sister. \"She always helps me.\"\n"
        "Charlie is Dave's friend. \"We play soccer together.\""
    )
    result = extractor.postprocess_text_spacy(text)
    assert result == [
        ("Alice", "Bob", "sister", '"She always helps me."'),
        ("Charlie", "Dave", "friend", '"We play soccer together."')
    ]

def test_incomplete_line(extractor):
    text = "Alice is Bob's sister."
    result = extractor.postprocess_text_spacy(text)
    assert result == []

def test_no_people_entities(extractor):
    text = "The cat is on the mat. \"It looks comfortable.\""
    result = extractor.postprocess_text_spacy(text)
    assert result == []

def test_relationship_with_extra_whitespace(extractor):
    text = "  Alice   is   Bob's   sister.   \"She always helps me.\"  "
    result = extractor.postprocess_text_spacy(text)
    assert result == [("Alice", "Bob", "sister", '"She always helps me."')]

def test_relationship_with_no_quotes(extractor):
    text = "Alice is Bob's sister. She always helps me."
    result = extractor.postprocess_text_spacy(text)
    assert result == [("Alice", "Bob", "sister", "She always helps me.")]

def test_relationship_with_complex_sentence(extractor):
    text = "Alice, who is Bob's sister, went to the park. \"She loves the outdoors.\""
    result = extractor.postprocess_text_spacy(text)
    assert result == [("Alice", "Bob", "sister", '"She loves the outdoors."')]

def test_empty_text(extractor):
    text = ""
    result = extractor.postprocess_text_spacy(text)
    assert result == []

def test_partial_relationship_pattern(extractor):
    text = "Alice and Bob. \"They are close.\""
    result = extractor.postprocess_text_spacy(text)
    assert result == []