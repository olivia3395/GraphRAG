from pathlib import Path
import chromadb
from typing import List, Dict, Any


class ChromaVectorStore:
    def __init__(self, persist_dir: str, collection_name: str):
        Path(persist_dir).mkdir(parents=True, exist_ok=True)
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection = self.client.get_or_create_collection(name=collection_name)

    def add(self, ids: List[str], embeddings: List[List[float]], documents: List[str], metadatas: List[Dict[str, Any]]):
        if not ids:
            return
        existing = set()
        try:
            res = self.collection.get(ids=ids)
            existing = set(res.get("ids", []))
        except Exception:
            existing = set()

        filtered = [
            (i, e, d, m)
            for i, e, d, m in zip(ids, embeddings, documents, metadatas)
            if i not in existing
        ]
        if not filtered:
            return
        f_ids, f_embs, f_docs, f_meta = zip(*filtered)
        self.collection.add(
            ids=list(f_ids),
            embeddings=list(f_embs),
            documents=list(f_docs),
            metadatas=list(f_meta),
        )

    def query(self, query_embedding: List[float], n_results: int = 5):
        return self.collection.query(query_embeddings=[query_embedding], n_results=n_results)

    def count(self) -> int:
        return self.collection.count()
