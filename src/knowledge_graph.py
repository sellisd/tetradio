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
        return [f"{n} : {v} : {e}" for n, v, e in self.G.edges]

    def save_dot(self, path="knowledge_graph.dot"):
        nx.nx_pydot.write_dot(self.G, path)
        logger.info(f"Knowledge graph saved to {path}")

    def save_dot_with_labels(self, path="knowledge_graph.dot"):
        pydot_graph = nx.nx_pydot.to_pydot(self.G)
        for edge in pydot_graph.get_edges():
            # The edge key is stored as 'key' in the NetworkX MultiDiGraph
            rel = edge.get('key')
            edge.set_label(rel)
        pydot_graph.write_raw(path)
        logger.info(f"Knowledge graph saved to {path}")