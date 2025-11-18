from loguru import logger
import spacy
from llm_interface import extract_relationships  # Import the function

def main():
    # Load text and spaCy model
    with open("src/sample_text.txt", "r", encoding="utf-8") as f:
        text = f.read()
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    [entity for entity in doc.ents if entity.label_ == "PERSON"]

    # Split text into paragraphs
    paragraphs = [p for p in text.split('\n\n') if p.strip()]

    results = []

    for paragraph in paragraphs:
        logger.info(f"Paragraph: {paragraph}")

        relationships = extract_relationships(paragraph)
        logger.info(f"Relationships: {relationships}")

    return results

if __name__ == "__main__":
    output = main()
    for item in output:
        print(f"Paragraph: {item['paragraph']}")
        print(f"Entities: {item['entities']}")
        if "relationships" in item:
            print(f"Relationships: {item['relationships']}")
        print()