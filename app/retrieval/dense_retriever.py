from typing import List, Dict, Any


class DenseTextRetriever:
    def __init__(self, embedder, vector_store):
        self.embedder = embedder
        self.vector_store = vector_store

    def retrieve(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        q = self.embedder.encode([query])[0].tolist()
        results = self.vector_store.query(query_embedding=q, n_results=top_k)

        out = []
        ids = results.get("ids", [[]])[0]
        docs = results.get("documents", [[]])[0]
        metas = results.get("metadatas", [[]])[0]
        dists = results.get("distances", [[]])[0]
        for i, doc_id in enumerate(ids):
            dist = float(dists[i]) if i < len(dists) else 0.0
            out.append(
                {
                    "id": doc_id,
                    "score": float(1.0 / (1.0 + dist)),
                    "content": docs[i],
                    "metadata": metas[i],
                }
            )
        return out
