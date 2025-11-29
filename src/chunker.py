import spacy

def split_text_by_sentence_chunks(text, chunk_length=1000, spacy_model="en_core_web_sm"):
    """
    Splits text into chunks of approximately `chunk_length` characters,
    ensuring that sentences are not split across chunks using spaCy for sentence detection.
    Consecutive chunks overlap by one sentence or 50 characters (whichever is smallest).

    Args:
        text (str): The input text to split.
        chunk_length (int): Target character length for each chunk.
        spacy_model (str): The spaCy model to use for sentence segmentation.

    Returns:
        List[str]: List of text chunks, each containing one or more complete sentences.
    """
    nlp = spacy.load(spacy_model)
    doc = nlp(text)
    sentences = [sent.text.strip() for sent in doc.sents if sent.text.strip()]
    chunks = []
    i = 0
    n = len(sentences)
    while i < n:
        current_chunk = sentences[i]
        j = i + 1
        while j < n and len(current_chunk) + len(sentences[j]) + 1 <= chunk_length:
            current_chunk += " " + sentences[j]
            j += 1
        # Determine overlap: one sentence or 50 characters, whichever is smallest
        if j < n:
            overlap_sentence = sentences[j-1]
            overlap_len = min(len(overlap_sentence), 50)
            # Find the overlap start index in the chunk
            overlap_start = len(current_chunk) - overlap_len
            if overlap_start < 0:
                overlap_start = 0
            # Find the sentence index to start next chunk
            if len(overlap_sentence) <= 50:
                next_i = j - 1  # overlap by one sentence
            else:
                # Overlap by 50 characters: find which sentence contains the overlap
                chars = 0
                for k in range(j-1, i-1, -1):
                    chars += len(sentences[k]) + (1 if k != j-1 else 0)
                    if chars >= 50:
                        next_i = k
                        break
                else:
                    next_i = i
        else:
            next_i = n  # End of text
        chunks.append(current_chunk)
        if next_i == i:
            # Avoid infinite loop if chunk is too small
            i += 1
        else:
            i = next_i
    return chunks