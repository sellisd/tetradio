# llm_interface.py
from loguru import logger
from typing import Dict, Any, List
from ollama import chat
import spacy

# --- Prompt construction ---
def build_relationship_prompt(chunk: str, current_relationships) -> str:
    """
    Constructs the prompt for relationship extraction.
    """
    relationship_context = ""
    if current_relationships:
        relationship_context = (
            "Context:\n"
            "Below are existing relationships in the knowledge graph. Use this information to avoid duplication and to infer new relationships if relevant.\n"
            "Existing relationships:\n"
            f"{current_relationships}\n"
            "When extracting relationships, consider:\n"
            "- If a relationship already exists in the knowledge graph do not repeat it in the output\n"
            "- Use existing relationships to infer indirect connections if logically possible.\n"
            "- Do NOT include any explanations, headers or extra text in your response.\n"
            )
    prompt = (
        "Task: Extract all family and romantic relationships between people mentioned in the text.\n"
        "Output will be used to populate a knowledge graph.\n\n"
        "Instructions:\n\n"
        "1. Include any relationship that is explicitly stated, implicitly stated, or logically inferrable from the text.\n"
        "2. If no relationships are present, return an empty string\n"
        "3. Do NOT include vague or unknown relationships such as \"unknown\", \"none\".\n"
        "4. List each relationship on a separate line in the format:\n"
        "   PersonA : PersonB : Relationship of PersonA to PersonB\n"
        "5. Standardize names: if the same person appears under multiple references, determine and use a canonical name based on strongest textual evidence.\n"
        "6. Do not use pronouns alone to identify individuals; resolve them to proper names where possible.\n"
        "7. Standardize relationship terms to common familial or romantic terms (e.g., mother, father, sister, brother, spouse, partner, fiancé, etc.).\n"
        "8. Include only human-to-human family or romantic connections.\n"
        " - No relationships to unnamed or collective entities.\n"
        "Example Text:\n"
        "  Natalia is the mother of Orion. Orion has a sister named Leila.\n"
        "Example Output:\n"
        "  Natalia : Orion : mother\n"
        "  Orion : Leila : brother\n"
        "  Leila : Natalia : daughter\n"
        f"{relationship_context}"
        "\nThe text from which the relationships are to be extracted follows.\n"
        "Text:\n"
        f"{chunk}"
    )
    return prompt


# --- Main extraction function ---
def extract_relationships(chunk: str, current_relationships: List[str], model_name: str = "gemma3") -> Dict[str, Any]:
    logger.info(f"Extracting relationships from text chunk: '{chunk[:50]} ... {chunk[-50:]}'")
    prompt = build_relationship_prompt(chunk, current_relationships)
    logger.debug(f"Constructed Prompt: {prompt}")
    llm = chat(model=model_name, messages=[
        {"role": "user", "content": prompt}
    ])
    response = parse_return_string(llm.message.content)
    return response

def parse_return_string(response: str):
    logger.info(f"Parsing LLM response: {response}")
    relationships = []
    for line in response.strip().splitlines():
        parts = [p.strip() for p in line.split(":")]
        logger.debug(f"Parsing line: {line} -> {parts}")
        if len(parts) == 3:
            person_a, person_b, relationship = parts
            logger.debug(f"Parsed relationship: {person_a} -> {person_b} ({relationship})")
            relationships.append((person_a, person_b, relationship))
        else:
            logger.warning(f"Line does not match expected format: {line}")
    logger.info(f"Extracted relationships: {relationships}")
    return relationships
