from loguru import logger
from chunker import chunk_book
from llm_interface import extract_relationships


def main():
    # Chunk the sample book
    with open("src/sample_text.txt", "r", encoding="utf-8") as f:
        text = f.read()
    chunks = chunk_book(text)
    logger.info(f"Generated {len(chunks)} chunks.")
    # Extract relationships/entities from each chunk
    person = {}
    from llm_interface import extract_relationships, extract_entities_spacy
    for chunk in chunks:
        logger.info("Extracting from chunk...")
        result = extract_entities_spacy(chunk)
        # result = extract_relationships(chunk)
        logger.info(f"Extraction result: {result}")
        person.update(result)
    results = person
    logger.info(f"Extracted results from {len(results)} chunks.")
    print(results)

if __name__ == "__main__":
    # Change method to "spacy" to use spaCy extractor
    main()