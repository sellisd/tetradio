from loguru import logger
from chunker import chunk_book
from llm_interface import extract_relationships


def main():
    # Chunk the sample book
    with open("src/sample_text.txt", "r", encoding="utf-8") as f:
        text = f.read()
    chunks = chunk_book(text)
    logger.info(f"Generated {len(chunks)} chunks.")
    # Extract relationships from each chunk
    results = []
    for chunk in chunks:
        logger.info("Extracting relationships from chunk...")
        logger.info(f"Chunk content: {chunk}")  # Log first 100 characters of the chunk
        extract_relationships(chunk)
        results.append(extract_relationships(chunk))
        logger.info("Extraction complete.")

    logger.info(f"Extracted relationships from {len(results)} chunks.")
    print(results)

if __name__ == "__main__":
    main()