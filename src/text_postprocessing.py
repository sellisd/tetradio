from loguru import logger
from ollama import chat

def advanced_postprocess_text(text: str) -> tuple:
    """
    Postprocess and format the text.
    """
    prompt = (
        "Task: Extract the relationship, if any, of two people from the following text and return it in the format:\n"
        "'Person A : Person B : Relationship of person A with person B'\n\n"
        "Instructions:\n"
        "- Use the exact format above, separating each part with a colon and a space.\n"
        "- Use proper names for both Person A and Person B.\n"
        "- Clearly state the relationship from Person A's perspective, if there is a relationship.\n"
        "- Only extract a relationship if the text explicitly describes a relationship between the two people.\n"
        "- If the input merely mentions two names without describing a relationship, return an empty string.\n"
        "- If the input does not describe a relationship, return an empty string.\n"
        "- Do NOT return anything if there is no clear relationship described.\n"
        "- Do NOT infer or guess a relationship if it is not explicitly stated in the text.\n"
        "- For example, if the input is just two names (e.g., 'Alice and Bob.'), return an empty string.\n\n"
        "Examples:\n"
        "Input: Alice is Bob's sister.\n"
        "Output: Alice : Bob : sister\n\n"
        "Input: Bob and Carol are colleagues.\n"
        "Output: Bob : Carol : colleague\n\n"
        "Input: Alice : Bob : sister\n"
        "Output: Alice : Bob : sister\n"
        "Input: The weather is nice today.\n"
        "Output: \n"
        "Input: Alice and Bob.\n"
        "Output: \n\n"
        "Now, process the following text:\n"
        f"Input: {text}"
        )
    response = chat(model="gemma3", messages=[
        {"role": "user", "content": prompt}
    ])
    logger.debug(prompt)
    logger.debug(response.message.content)
    formatted_line = response.message.content.strip()
    parts = [p.strip() for p in formatted_line.split(":")]
    response = ()
    if len(parts) == 3 and all(parts):
        person_a, person_b, relationship = parts
        # Filter out "No relationship" or similar non-relationships
        if relationship.strip().lower() in ["no relationship", "none", ""]:
            logger.info(f"Filtered out non-relationship: {person_a} -> {person_b} ({relationship})")
            response = ()
        else:
            logger.info(f"Parsed relationship: {person_a} -> {person_b} ({relationship})")
            response = (person_a, person_b, relationship)
    else:
        logger.warning(f"Formatted line does not match expected format: {formatted_line}")
    return response  # Return empty tuple if format is incorrect