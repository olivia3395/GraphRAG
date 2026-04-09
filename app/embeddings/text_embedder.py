from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np


class TextEmbedder:
    def __init__(self, model_name: str):
        self.model = SentenceTransformer(model_name)

    def encode(self, texts: List[str]) -> np.ndarray:
        if not texts:
            return np.empty((0, 384), dtype=float)
        return self.model.encode(texts, normalize_embeddings=True)
