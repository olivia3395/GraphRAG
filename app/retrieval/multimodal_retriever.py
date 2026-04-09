from typing import List, Dict, Any


class MultimodalRetriever:
    def __init__(self, image_embedder, image_store):
        self.image_embedder = image_embedder
        self.image_store = image_store

    def retrieve_images(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        q = self.image_embedder.encode_texts([query])[0].tolist()
        results = self.image_store.query(query_embedding=q, n_results=top_k)

        out = []
        ids = results.get("ids", [[]])[0]
        docs = results.get("documents", [[]])[0]
        metas = results.get("metadatas", [[]])[0]
        dists = results.get("distances", [[]])[0]
        for i, item_id in enumerate(ids):
            dist = float(dists[i]) if i < len(dists) else 0.0
            out.append(
                {
                    "id": item_id,
                    "score": float(1.0 / (1.0 + dist)),
                    "content": docs[i],
                    "metadata": metas[i],
                }
            )
        return out
