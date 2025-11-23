def split_paragraphs_sliding_window(text, window_size=2, min_chunk_length=200):
    """
    Splits text into overlapping chunks using a sliding window over paragraphs.

    Each chunk consists of `window_size` consecutive paragraphs. If the resulting
    chunk is shorter than `min_chunk_length` characters, additional paragraphs
    are appended until the minimum length is reached or no more paragraphs remain.

    Args:
        text (str): The input text to split, paragraphs separated by double newlines.
        window_size (int): Number of paragraphs in each initial chunk window.
        min_chunk_length (int): Minimum character length for each chunk.

    Returns:
        List[str]: List of text chunks, each containing one or more paragraphs.
    """
    paragraphs = [p for p in text.split('\n\n') if p.strip()]
    chunks = []
    i = 0
    while i < len(paragraphs):
        chunk_paragraphs = paragraphs[i:i+window_size]
        chunk = '\n\n'.join(chunk_paragraphs)
        # If chunk is too short, try to add more paragraphs
        j = i + window_size
        while len(chunk) < min_chunk_length and j < len(paragraphs):
            chunk_paragraphs.append(paragraphs[j])
            chunk = '\n\n'.join(chunk_paragraphs)
            j += 1
        chunks.append(chunk)
        i += 1
    return chunks
