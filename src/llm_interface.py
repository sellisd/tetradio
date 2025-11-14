# llm_interface.py

from typing import Dict, Any
from ollama import chat


# --- Prompt construction ---
def build_relationship_prompt(chunk: str) -> str:
    """
    Constructs the prompt for relationship extraction.
    """
    return (
        "Extract all people mentioned in the following text and describe their relationships. "
        "Return a JSON object with 'heroes' (list of names) and 'relationships' (list of {parent, child} pairs):\n"
        f"{chunk}"
    )


# --- Main extraction function ---
def extract_relationships(chunk: str, model_name: str = "gemma3") -> Dict[str, Any]:
    prompt = build_relationship_prompt(chunk)
    llm = chat(model=model_name, messages=[
        {"role": "user", "content": prompt}
    ])
    
    return llm.message.content
