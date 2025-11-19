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
    prompt = (
        "Extract all family and romantic relationships between people mentioned in the following text.\n"
        "Instructions:\n"
        "- If a relationship is stated, implied, or can logically be inferred, include it.\n"
        "- If no relationships are found, return an empty string\n"
        "- For each relationship, use the format:\n"
        "  PersonA : PersonB : Relationship of PersonA to PersonB\n"
        "Example:\n"
        "  Natalia : Orion : mother\n"
        "\nText:\n"
        f"{chunk}"
    )
    return prompt


# --- Main extraction function ---
def extract_relationships(chunk: str, model_name: str = "gemma3") -> Dict[str, Any]:
    logger.info(f"Extracting relationships from text chunk: '{chunk[:50]} ... {chunk[-50:]}'")
    prompt = build_relationship_prompt(chunk)
    llm = chat(model=model_name, messages=[
        {"role": "user", "content": prompt}
    ])
    response = parse_return_string(llm.message.content)
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
