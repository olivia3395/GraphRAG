from app.graph.entity_extractor import SimpleEntityExtractor
from app.graph.graph_builder import KnowledgeGraphBuilder
from app.ingestion.loaders import load_text_file
from app.utils.file_utils import list_text_files


def main():
    extractor = SimpleEntityExtractor()
    builder = KnowledgeGraphBuilder()
    for path in list_text_files("./data/demo"):
        text = load_text_file(path)
        entities = extractor.extract(text)
        builder.add_chunk_entities(str(path), entities, {"source": str(path), "content": text[:500]})
        builder.connect_cooccurring_entities(entities)
    print(f"Graph built with {builder.graph.number_of_nodes()} nodes and {builder.graph.number_of_edges()} edges")


if __name__ == "__main__":
    main()
