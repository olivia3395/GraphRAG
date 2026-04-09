from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseModel):
    app_name: str = "OmniGraphRAG"
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "8000"))

    chroma_text_collection: str = "text_chunks"
    chroma_image_collection: str = "image_items"
    chroma_persist_dir: str = "./data/processed/chroma"

    text_embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    image_embedding_model: str = "openai/clip-vit-base-patch32"

    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

    chunk_size: int = 500
    chunk_overlap: int = 100


settings = Settings()
