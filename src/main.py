from loguru import logger
from chunker import chunk_book
from llm_interface import extract_relationships

SAMPLE_TEXT = '''
Achilles was the son of Peleus. Peleus was a great hero.
'''

def main():
    # Chunk the sample book
    chunks = chunk_book(SAMPLE_TEXT)
    logger.info(f"Generated {len(chunks)} chunks.")
    # Extract relationships from each chunk
    results = [extract_relationships(chunk) for chunk in chunks]
    logger.info(f"Extracted relationships from {len(results)} chunks.")
    print(results)

if __name__ == "__main__":
    main()