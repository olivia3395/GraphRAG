from app.core.config import settings
from app.embeddings.text_embedder import TextEmbedder
from app.embeddings.image_embedder import ImageEmbedder
from app.stores.vector_store import ChromaVectorStore
from app.stores.image_store import ImageStore
from app.graph.entity_extractor import SimpleEntityExtractor
from app.graph.graph_builder import KnowledgeGraphBuilder
from app.ingestion.pipeline import IngestionPipeline


def main():
    text_embedder = TextEmbedder(settings.text_embedding_model)
    image_embedder = ImageEmbedder(settings.image_embedding_model)
    text_store = ChromaVectorStore(settings.chroma_persist_dir, settings.chroma_text_collection)
    image_store = ImageStore(settings.chroma_persist_dir, settings.chroma_image_collection)
    entity_extractor = SimpleEntityExtractor()
    graph_builder = KnowledgeGraphBuilder()

    pipeline = IngestionPipeline(
        text_embedder=text_embedder,
        image_embedder=image_embedder,
        text_store=text_store,
        image_store=image_store,
        entity_extractor=entity_extractor,
        graph_builder=graph_builder,
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
    )
    result = pipeline.ingest("./data/demo")
    print("Index build complete:", result)


if __name__ == "__main__":
    main()
