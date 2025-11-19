import networkx as nx
from loguru import logger

class KnowledgeGraph:
    def __init__(self):
        self.G = nx.MultiDiGraph()

    def add_relationship(self, person_a, person_b, relationship):
        if self.G.has_edge(person_a, person_b, relationship):
            logger.info(f"Edge already exists: {person_a} -[{relationship}]-> {person_b}")
        else:
            logger.info(f"Adding edge: {person_a} -[{relationship}]-> {person_b}")
            self.G.add_edge(person_a, person_b, relationship)

    def get_relationships(self):
        return [f"{n} : {v} : {e.get('label')}" for n, v, e in self.G.edges(data=True)]

    def save_dot(self, path="knowledge_graph.dot"):
        nx.nx_pydot.write_dot(self.G, path)
        logger.info(f"Knowledge graph saved to {path}")