def chunk_book(text: str, chunk_size: int = 1800, overlap: int = 300):
    """
    Splits the input text into overlapping chunks of words.
    Args:
        text (str): The full text.
        chunk_size (int): Number of words per chunk.
        overlap (int): Number of words to overlap between chunks.
    Returns:
        List[str]: List of text chunks.
    """
    words = text.split()
    chunks = []
    start = 0
    total_words = len(words)
    while start < total_words:
        end = min(start + chunk_size, total_words)
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        if end == total_words:
            break
        start = max(end - overlap, 0)
    return chunks