from loguru import logger
from ollama import chat
from fast import RelationshipExtractor

def generate_relationship_graph_and_excerpt(style):
    # Step 1: Generate relationship graph (as text)
    graph_prompt = (
        f"You are an expert literary analyst. Your task is to create a genealogical or relationship graph of heroes inspired by the style of '{style}'.\n"
        "Instructions:\n"
        "1. List relationships between characters as plain English sentences, one per line.\n"
        "2. Use clear, direct statements (e.g., 'John is the father of Mary.' 'Mary is the wife of Paul.').\n"
        "3. Only include relationships relevant to the style and themes of the source.\n"
        "4. Do not invent unnecessary details; keep the relationships plausible and concise.\n"
        "Output:\n"
        "A list of relationship sentences as described above."
        "Limit the output to 5 relationships"
        )
    logger.info("Generating relationship graph...")
    graph_response = chat(model='gemma3', messages=[
        {"role": "user", "content": graph_prompt}
    ])
    graph_text = graph_response.message.content
    logger.info(f"Generated Graph Text: {graph_text}")
    # Step 2: Reformat graph_text to match extract_relationships output format
    reformat_prompt = (
        "You are a data formatter. Your task is to convert the following relationship descriptions into a Python list of tuples.\n"
        "Instructions:\n"
        "1. Each tuple should be in the format: (person1, person2, relationship).\n"
        "2. Use only the information provided; do not invent or infer additional relationships.\n"
        "3. Preserve the directionality of the relationship, e.g., (John, Mary, father) means John is the father of Mary.\n"
        "4. Use clear, consistent naming for characters.\n"
        "5. Output only the Python list of tuples, nothing else.\n"
        "Example:\n"
        "[('John', 'Mary', 'wife'), ('Paul', 'Mary', 'husband')]\n"
        "Relationships:\n"
        f"{graph_text}"
    )
    reformat_response = chat(model='gemma3', messages=[
        {"role": "user", "content": reformat_prompt}
    ])
    reformatted_graph = reformat_response.message.content
    logger.info(f"Reformatted Graph: {reformatted_graph}")
    # Step 3: Generate a paragraph in the style of the book mentioning these relationships
    excerpt_prompt = (
        f"You are an expert novelist. Write a single, coherent paragraph in the style of '{style}'.\n"
        "Requirements:\n"
        "1. Naturally mention the relationships listed below, weaving them into the narrative.\n"
        "2. Do not list the relationships mechanically; integrate them as part of the story or character interactions.\n"
        "3. Use language, tone, and themes consistent with the style.\n"
        "4. Do not invent additional relationships or characters.\n"
        "5. Limit the excerpt to one paragraph.\n"
        "Relationships:\n"
        f"{graph_text}"
    )
    excerpt_response = chat(model='gemma3', messages=[
        {"role": "user", "content": excerpt_prompt}
    ])
    excerpt_text = excerpt_response.message.content
    logger.info(f"Generated Excerpt: {excerpt_text}")
    # Step 4: Extract relationships from the excerpt
    extractor = RelationshipExtractor()
    relationships = extractor.extract_relationships(excerpt_text)
    logger.info(f"Extracted Relationships: {relationships}")

def main():
    style = "Middlemarch by George Eliot"
    results = generate_relationship_graph_and_excerpt(style)

if __name__ == "__main__":
    main()
