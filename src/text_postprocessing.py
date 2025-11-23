from loguru import logger
from ollama import chat

def advanced_postprocess_text(text: str) -> tuple:
    """
    Postprocess and format the text.
    """
    prompt = (
        "Task: Extract the relationship of two people from the following text and return it in the format:\n"
        "'Person A : Person B : Relationship of person A with person B\n\n"
        "Instructions:\n"
        "- Use the exact format above, separating each part with a colon and a space.\n"
        "- Use proper names for both Person A and Person B.\n"
        "- Clearly state the relationship from Person A's perspective.\n"
        "- If the input is already in the correct format, return it unchanged.\n"
        "- If the input does not describe a relationship, return an empty string.\n"
        "Example:\n"
        "Input: Alice is Bob's sister.\n"
        "Output: Alice : Bob : sister\n\n"
        "Input: Bob and Carol are colleagues.\n"
        "Output: Bob : Carol : colleague\n\n"
        "Input: Alice : Bob : sister\n"
        "Output: Alice : Bob : sister\n"
        "Input: The weather is nice today.\n"
        "Output: \n\n"
        f"Input: {text}"
        )
    response = chat(model="gemma3", messages=[
        {"role": "user", "content": prompt}
    ])
    formatted_line = response.message.content.strip()
    parts = [p.strip() for p in formatted_line.split(":")]
    response = ()
    if len(parts) == 3 and all(parts):
        person_a, person_b, relationship = parts
        logger.info(f"Parsed relationship: {person_a} -> {person_b} ({relationship})")
        response = (person_a, person_b, relationship)
    else:
        logger.warning(f"Formatted line does not match expected format: {formatted_line}")
    return response  # Return empty tuple if format is incorrect