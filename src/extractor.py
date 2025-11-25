import spacy
import re

from loguru import logger
from typing import List
from ollama import chat

from text_postprocessing import advanced_postprocess_text
from tools import text_normalize

class Extractor:

    def __init__(self, source: str, model_name: str = "gemma3"):
        self.model_name = model_name
        self.source = source


    def summarize_relationships(self) -> str:
        """
        Constructs the prompt for relationship extraction.
        """
        prompt = (
            "Task: Extract family relationships between people mentioned in the text and quote the original source that supports this.\n"
            "Instructions:\n\n"
            "1. Include any relationship that is explicitly stated in the text.\n"
            "2. List each relationship on a separate line\n"
            "3. On the same line, after the relationship include a quoted text snippet from the original text that supports this relationship.\n"
            "4. If no relationships are present, return an empty string\n"
            "5. Do NOT include vague or unknown relationships such as \"unknown\", \"none\".\n"
            "6. Standardize names: if the same person appears under multiple references, determine and use a canonical name based on strongest textual evidence.\n"
            "7. Do not use pronouns alone to identify individuals; resolve them to proper names where possible.\n"
            "8. Standardize relationship terms to common kinship or family terms (e.g., mother, father, sister, brother, spouse, partner, fiancé, etc.).\n"
            "9. Include only human-to-human family connections.\n"
            "10. Do NOT include relationships to unnamed or collective entities.\n"
            "Example Text:\n"
            "  Natalia is the mother of Orion. Orion has a sister named Leila.\n"
            "Example Output:\n"
            "  Natalia is Orion's mother. 'Natalia is the mother of Orion.'\n"
            "  Orion is Leila's brother 'Orion has a sister named Leila.'\n"
            "\nThe text from which the relationships are to be extracted follows.\n"
            "Text:\n"
            f"{self.source}"
        )
        response = chat(model=self.model_name, messages=[
            {"role": "user", "content": prompt}])
        response.message.content
        return response.message.content


    def postprocess_text_spacy(self, text: str) -> List[tuple]:
        """
        Extract people, their relationships, and the quoted text using spaCy.
        Each line contains two sentences: 
        - The first sentence is used to extract people and relationships.
        - The second sentence is the quoted text and is extracted as is.
        """

        nlp = spacy.load("en_core_web_sm")
        relationships = []

        # Process each line in the text
        for line in text.splitlines():
            logger.info(f"Processing line: {line}")
            # Normalize whitespace
            line = re.sub(r'\s+', ' ', line.strip())
            # Split the line into two parts: the first sentence and the quoted text
            parts = re.split(r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.)\s+", line, maxsplit=1)
            if len(parts) < 2:
                logger.warning(f"Line does not contain two sentences: {line}")
                continue

            first_sentence, quoted_text = parts
            logger.debug(f"First sentence: {first_sentence}")
            logger.debug(f"Quoted text: {quoted_text}")
            
            # Check if quoted text is empty
            if not quoted_text.strip():
                logger.warning(f"No quoted text found in line: {line}")
                continue

            # Check if quoted text is a valid quote
            if text_normalize(quoted_text) not in text_normalize(self.source):
                logger.warning(f"Quoted text not found in source: {quoted_text}")
                continue

            # Process the first sentence with spaCy
            doc = nlp(first_sentence)
            people = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
            logger.debug(f"Identified people: {people}")

            # Use a simple heuristic to find relationships
            match = re.search(r"(\w+) is (\w+)'s (\w+)", first_sentence)
            if match and len(match.groups()) == 3:
                person_a = match.group(1)
                person_b = match.group(2)
                relationship = match.group(3)

                # Final validation step to ensure person_a and person_b are labeled as PERSON
                if person_a in people and person_b in people:
                    logger.debug(f"Validated relationship: {person_a} -> {person_b} ({relationship})")
                    relationships.append((person_a, person_b, relationship, quoted_text.strip()))
                else:
                    logger.warning(f"Extracted names are not labeled as PERSON: {person_a}, {person_b}")
                    tripple = advanced_postprocess_text(first_sentence)
                    if tripple:
                        relationships.append(tripple+(quoted_text.strip(),))
            else:
                logger.warning(f"No valid relationship found in sentence: {first_sentence}")
                tripple = advanced_postprocess_text(first_sentence)
                if tripple:
                    relationships.append(tripple+(quoted_text.strip(),))
        return relationships
