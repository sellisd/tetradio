import sys
print("PYTHONPATH:", sys.path)
import pytest
from fast import RelationshipExtractor

EXAMPLE_TEXT = """
The rain, as it often did in Tilling Manor’s vicinity, seemed to mirror the perpetual dampness of Edward Casaubon’s soul – a dampness exacerbated, perhaps, by the insistent, almost disapproving glances of his daughter, Lucy, who sat by the fire, meticulously copying extracts from the Institutes, a task she felt obligated to undertake, not out of any genuine interest, but a dutiful response to her father's meticulous, and ultimately, isolating, world. Walter Langham, a man weary of the unspoken tensions that had always marked his relationship with both Edward and Lucy – tensions rooted in the shared blood of Silas Casaubon and a profound, unacknowledged affection for Lucy herself – paced the hearth, acutely aware of Mary Garth’s quiet presence as she assisted Josiah Wild, her step-father, with the repairs to the barn – a task performed with a practicality that seemed to mock the sterile erudition of the Manor. Even Edward, lost in the labyrinthine corridors of his own intellect, seemed to register, if only with a flicker of distaste, the steady, unwavering devotion of Mary Garth to Walter, a devotion built upon a shared understanding of rural hardship and a quiet resilience that offered a stark contrast to the brittle, self-contained existence he fostered for his children, a life where the very bonds of family – Lucy, Walter, and Silas – seemed perpetually strained by an inherited, and ultimately unresolvable, melancholy.
"""

def test_relationship_extractor():
    extractor = RelationshipExtractor()
    relationships = extractor.extract_relationships(EXAMPLE_TEXT)
    # Example expected relationships (update as needed)
    expected = [
        ("Edward Casaubon", "Lucy", "father"),
        ("Edward", "Lucy", "father"),
        ("Josiah Wild", "Mary", "step-father"),
    ]
    breakpoint()
    for rel in expected:
        assert rel in relationships
print("EXAMPLE_TEXT:", EXAMPLE_TEXT)
extractor = RelationshipExtractor()
print("Extracted relationships:", extractor.extract_relationships(EXAMPLE_TEXT))