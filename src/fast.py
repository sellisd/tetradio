from ollama import chat
from loguru import logger
class RelationshipExtractor:
    def extract_relationships(self, text, model_name="gemma3"):
        logger.info("Starting LLM relationship extraction")
        prompt = (
            "You are an expert relationship extractor. "
            "Your task is to identify all explicit or logically inferred family or romantic relationships in the provided text. "
            "For each relationship, output a tuple in the format: (Person1, Person2, Relationship). "
            "Only include relationships that are clearly stated or can be directly inferred from the text. "
            "Do not guess or invent relationships. "
            "List each tuple on a separate line. "
            "Examples:\n"
            "(Natalia, Orion, mother)\n"
            "(John, Mary, wife)\n"
            "(Alice, Bob, boyfriend)\n"
            "Text:\n"
            f"{text}\n"
            "Extracted relationships:"
        )
        response = chat(model=model_name, messages=[
            {"role": "user", "content": prompt}
        ])
        content = response.message.content
        logger.info(f"LLM Response for relationship extraction: {content}")
        relationships = []
        
        import re
        tuple_pattern = re.compile(r"\(\s*([^)]+?)\s*,\s*([^)]+?)\s*,\s*([^)]+?)\s*\)")
        for line in content.strip().splitlines():
            line = line.strip()
            match = tuple_pattern.match(line)
            if match:
                person1 = match.group(1).strip()
                person2 = match.group(2).strip()
                relation = match.group(3).strip()
                relationships.append((person1, person2, relation))
            else:
                logger.warning(f"Failed to parse line: {line}")
        logger.info(f"Parsed relationships: {relationships}")
        logger.info("Finished LLM relationship extraction")
        return relationships

# Example usage:
# extractor = RelationshipExtractor()
# print(extractor.extract_relationships("John's wife Mary went to the store."))