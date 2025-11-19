# llm_interface.py
from loguru import logger
from typing import Dict, Any
from ollama import chat
import spacy

# --- Prompt construction ---
def build_relationship_prompt(chunk: str) -> str:
    """
    Constructs the prompt for relationship extraction.
    """
    return (
        "In the following text extract the family or romantic relationships of people mentioned. If no relationship is"
        "stated, implied or can logically be inferred, return no relationship."
        "Return all pairwise relationships following the format: 'PersonA : PersonB : Relationship of PersonA to PersonB'"
        "for example 'Natalia : Orion : mother' to express that Natalia is the mother of Orion.\n\n"
        f"{chunk}"
    )


# --- Main extraction function ---
def extract_relationships(chunk: str, model_name: str = "gemma3") -> Dict[str, Any]:
    prompt = build_relationship_prompt(chunk)
    llm = chat(model=model_name, messages=[
        {"role": "user", "content": prompt}
    ])
    response = parse_return_string( llm.message.content)
    logger.info(f"LLM Response: {response}")
    return response

def parse_return_string(response: str):
    relationships = []
    for line in response.strip().splitlines():
        parts = [p.strip() for p in line.split(":")]
        if len(parts) == 3:
            person_a, person_b, relationship = parts
            relationships.append((person_a, person_b, relationship))
    return relationships
