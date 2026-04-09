from typing import Dict, Any
from app.retrieval.reranker import simple_rerank


class HybridRetriever:
    def __init__(self, text_retriever, image_retriever, entity_extractor, graph_retriever, graph_builder):
        self.text_retriever = text_retriever
        self.image_retriever = image_retriever
        self.entity_extractor = entity_extractor
        self.graph_retriever = graph_retriever
        self.graph_builder = graph_builder

    def retrieve(self, query: str, top_k_text: int = 5, top_k_image: int = 3, graph_hops: int = 1, use_multimodal: bool = True) -> Dict[str, Any]:
        text_hits = self.text_retriever.retrieve(query, top_k=top_k_text)
        image_hits = self.image_retriever.retrieve_images(query, top_k=top_k_image) if use_multimodal else []

        query_entities = self.entity_extractor.extract(query)
        expanded_nodes = self.graph_retriever.expand_from_entities(query_entities, hops=graph_hops)

        graph_chunk_hits = []
        for node in expanded_nodes:
            if node in self.graph_builder.graph.nodes:
                attrs = self.graph_builder.graph.nodes[node]
                if attrs.get("node_type") == "chunk":
                    graph_chunk_hits.append(
                        {
                            "id": node,
                            "score": 0.35,
                            "content": attrs.get("content", ""),
                            "metadata": {k: v for k, v in attrs.items() if k != "content"},
                        }
                    )

        seen = {x["id"] for x in text_hits}
        for item in graph_chunk_hits:
            if item["id"] not in seen:
                text_hits.append(item)

        text_hits = simple_rerank(query, text_hits)
        image_hits = sorted(image_hits, key=lambda x: x["score"], reverse=True)

        return {
            "text_hits": text_hits[: max(top_k_text + 3, len(text_hits))],
            "image_hits": image_hits[:top_k_image],
            "expanded_nodes": expanded_nodes,
        }
