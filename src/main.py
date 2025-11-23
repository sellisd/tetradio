import sys
from loguru import logger
from extractor import Extractor
from knowledge_graph import KnowledgeGraph
from chunker import split_paragraphs_sliding_window

logger.remove()
logger.add("app.log", level="DEBUG", mode="w")
logger.add(sys.stdout, level="INFO")

def main():
    KG = KnowledgeGraph()
    with open("data/chapter_1.txt", "r") as file:
        text = file.read()
        chunks = split_paragraphs_sliding_window(text, window_size=3, min_chunk_length=4000)
        for i, chunk in enumerate(chunks):
            logger.info(f"Processing chunk {i+1}/{len(chunks)}")
            extractor = Extractor(chunk, model_name="gemma3")
            logger.info(f"Extracting relationships from text chunk: '{chunk[:10]} ... {chunk[-10:]}'")
            summary = extractor.summarize_relationships()
            triples = extractor.postprocess_text_spacy(summary)
            for person_a, person_b, relationship in triples:
                KG.add_relationship(person_a, person_b, relationship)
            if i%5 == 0:
                KG.save_dot_with_labels(f"knowledge_graph_step_{i}.dot")
    KG.save_dot_with_labels("knowledge_graph.dot")

if __name__ == "__main__":
    main()
