from loguru import logger
from llm_interface import extract_relationships
from knowledge_graph import KnowledgeGraph

def split_paragraphs_sliding_window(text, window_size=2):
    paragraphs = [p for p in text.split('\n\n') if p.strip()]
    chunks = []
    for i in range(len(paragraphs) - window_size + 1):
        chunk = '\n\n'.join(paragraphs[i:i+window_size])
        chunks.append(chunk)
    return chunks

def main():
    KG = KnowledgeGraph()
    with open("src/sample_text.txt", "r") as file:
        text = file.read()
        chunks = split_paragraphs_sliding_window(text, window_size=2)
        for chunk in chunks:
            current_relationships = KG.get_relationships()
            triples = extract_relationships(chunk, current_relationships)
            for person_a, person_b, relationship in triples:
                KG.add_relationship(person_a, person_b, relationship)
    KG.save_dot_with_labels("knowledge_graph.dot")

if __name__ == "__main__":
    main()
