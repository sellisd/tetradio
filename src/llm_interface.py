# llm_interface.py
from loguru import logger
from typing import Dict, Any
from ollama import chat


# --- Prompt construction ---
def build_relationship_prompt(chunk: str) -> str:
    """
    Constructs the prompt for relationship extraction.
    """
    return (
        "In the following text extract names and relationships of people:\n\n"
        f"{chunk}"
    )


# --- Main extraction function ---
def extract_relationships(chunk: str, model_name: str = "gemma3") -> Dict[str, Any]:
    prompt = build_relationship_prompt(chunk)
    logger.info(f"Prompt for LLM: {prompt}")
    llm = chat(model=model_name, messages=[
        {"role": "user", "content": prompt}
    ])
    logger.info(f"LLM response: {llm.message.content}")
    return llm.message.content
