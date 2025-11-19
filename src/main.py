from loguru import logger
from llm_interface import extract_relationships
from knowledge_graph import KnowledgeGraph

def main():
    KG = KnowledgeGraph()
    with open("src/sample_text.txt", "r") as file:
        text = file.read()
        paragraphs = [p for p in text.split('\n\n') if p.strip()]
        for paragraph in paragraphs:
            current_relationships = KG.get_relationships()
            triples = extract_relationships(paragraph, current_relationships)
            for person_a, person_b, relationship in triples:
                KG.add_relationship(person_a, person_b, relationship)
    KG.save_dot("knowledge_graph.dot")

if __name__ == "__main__":
    main()
