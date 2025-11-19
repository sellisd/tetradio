import pytest
from knowledge_graph import KnowledgeGraph

def test_add_relationship():
    kg = KnowledgeGraph()
    # Add a relationship
    kg.add_relationship("Alice", "Bob", "parent")
    assert kg.get_relationships() == ["Alice : Bob : parent"]
    edges = list(kg.G.edges)
    assert len(edges) == 1
    assert edges[0][0] == "Alice"
    assert edges[0][1] == "Bob"
    assert edges[0][2] == "parent"
    # Add a duplicate relationship (should not create a new edge)
    kg.add_relationship("Alice", "Bob", "parent")
    edges_after_duplicate = list(kg.G.edges)
    assert len(edges_after_duplicate) == 1

    # Add a different relationship between same nodes
    kg.add_relationship("Alice", "Bob", "guardian")
    edges_final = list(kg.G.edges)
    # MultiDiGraph allows multiple edges, so now there should be 2
    assert len(edges_final) == 2
    labels = [e[2] for e in edges_final]
    assert "parent" in labels
    assert "guardian" in labels
