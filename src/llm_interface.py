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
            "- Do not repeat relationships already listed in the knowledge graph.\n"
            "- Use existing relationships to infer indirect connections if logically possible.\n"
            "- Do NOT include any explanations, headers or extra text in your response.\n"
            "Take into account the following existing relationships in the knowledge graph:\n"
            f"{current_relationships}"
           )
    prompt = (
        "Extract all family and romantic relationships between people mentioned in the following text in order to add them to a knowledge graph.\n"
        "Instructions:\n"
        "- If a relationship is stated, implied, or can logically be inferred, include it.\n"
        "- If no relationships are found, return an empty string\n"
        "- For each relationship, use the format:\n"
        "  PersonA : PersonB : Relationship of PersonA to PersonB\n"
        "Example:\n"
        "  Natalia : Orion : mother\n"
        f"{relationship_context}"
        "\nText:\n"
        f"{chunk}"
    )
    return prompt


# --- Main extraction function ---
def extract_relationships(chunk: str, current_relationships: List[str], model_name: str = "gemma3") -> Dict[str, Any]:
    logger.info(f"Extracting relationships from text chunk: '{chunk[:50]} ... {chunk[-50:]}'")
    prompt = build_relationship_prompt(chunk, current_relationships)
    #logger.info(f"Constructed Prompt: {prompt}")
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
        if len(parts) == 3:
            person_a, person_b, relationship = parts
            relationships.append((person_a, person_b, relationship))
    logger.info(f"Extracted relationships: {relationships}")
    return relationships
