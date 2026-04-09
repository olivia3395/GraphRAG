from fastapi import FastAPI

from app.core.config import settings
from app.api.routes_health import router as health_router
from app.api.routes_ingest import router as ingest_router, set_ingestion_pipeline
from app.api.routes_query import router as query_router, set_answer_pipeline

from app.embeddings.text_embedder import TextEmbedder
from app.embeddings.image_embedder import ImageEmbedder
from app.stores.vector_store import ChromaVectorStore
from app.stores.image_store import ImageStore
from app.graph.entity_extractor import SimpleEntityExtractor
from app.graph.graph_builder import KnowledgeGraphBuilder
from app.graph.graph_retriever import GraphRetriever
from app.retrieval.dense_retriever import DenseTextRetriever
from app.retrieval.multimodal_retriever import MultimodalRetriever
from app.retrieval.hybrid_retriever import HybridRetriever
from app.llm.generator import LLMGenerator
from app.llm.answer_pipeline import AnswerPipeline
from app.ingestion.pipeline import IngestionPipeline


app = FastAPI(title=settings.app_name)

text_embedder = TextEmbedder(settings.text_embedding_model)
image_embedder = ImageEmbedder(settings.image_embedding_model)
text_store = ChromaVectorStore(settings.chroma_persist_dir, settings.chroma_text_collection)
image_store = ImageStore(settings.chroma_persist_dir, settings.chroma_image_collection)
entity_extractor = SimpleEntityExtractor()
graph_builder = KnowledgeGraphBuilder()
graph_retriever = GraphRetriever(graph_builder)

text_retriever = DenseTextRetriever(text_embedder, text_store)
image_retriever = MultimodalRetriever(image_embedder, image_store)
hybrid_retriever = HybridRetriever(
    text_retriever=text_retriever,
    image_retriever=image_retriever,
    entity_extractor=entity_extractor,
    graph_retriever=graph_retriever,
    graph_builder=graph_builder,
)

generator = LLMGenerator(settings.openai_api_key, settings.openai_model)
answer_pipeline = AnswerPipeline(hybrid_retriever, generator)

ingestion_pipeline = IngestionPipeline(
    text_embedder=text_embedder,
    image_embedder=image_embedder,
    text_store=text_store,
    image_store=image_store,
    entity_extractor=entity_extractor,
    graph_builder=graph_builder,
    chunk_size=settings.chunk_size,
    chunk_overlap=settings.chunk_overlap,
)

set_ingestion_pipeline(ingestion_pipeline)
set_answer_pipeline(answer_pipeline)

app.include_router(health_router)
app.include_router(ingest_router)
app.include_router(query_router)
