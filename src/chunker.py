from spacy.lang.en import English

def chunk_book(text: str):
    """
    Splits the input text into sentences.
    Args:
        text (str): The full text.
    Returns:
        Generator object.
    """
    nlp = English()
    nlp.add_pipe("sentencizer")
    return nlp(text).sents