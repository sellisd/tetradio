import unicodedata
import re


def text_normalize(text):
    """
    Thoroughly normalizes a string for robust comparison:
    - Unicode normalization (NFKC)
    - Lowercasing
    - Remove punctuation
    - Remove special characters (non-alphanumeric, non-whitespace)
    - Normalize all whitespace to single spaces
    - Strip leading/trailing whitespace
    """
    # Unicode normalization
    text = unicodedata.normalize('NFKC', text)
    # Lowercase
    text = text.lower()
    # Remove punctuation and special characters (keep only alphanumerics and whitespace)
    text = re.sub(r'[^\w\s]', '', text)
    # Normalize all whitespace (spaces, tabs, newlines) to single spaces
    text = re.sub(r'\s+', ' ', text)
    # Strip leading/trailing whitespace
    text = text.strip()
    return text
