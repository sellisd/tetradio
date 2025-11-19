import networkx as nx
from loguru import logger
from llm_interface import extract_relationships


def main():
    G = nx.MultiDiGraph()
    with open("src/sample_text.txt", "r") as file:
        text = file.read()
        paragraphs = [p for p in text.split('\n\n') if p.strip()]
        for paragraph in paragraphs:
            triples = extract_relationships(paragraph)
            for person_a, person_b, relationship in triples:
                logger.info(f"Adding edge: {person_a} -[{relationship}]-> {person_b}")
                G.add_edge(person_a, person_b, label=relationship)
    nx.nx_pydot.write_dot(G, "knowledge_graph.dot") 
    logger.info("Knowledge graph saved to knowledge_graph.dot")

if __name__ == "__main__":
    main()
