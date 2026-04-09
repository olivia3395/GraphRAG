from typing import List, Dict, Any


def simple_rerank(query: str, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    query_terms = set(query.lower().split())
    for item in items:
        content_terms = set(item.get("content", "").lower().split())
        overlap = len(query_terms & content_terms)
        item["score"] = float(item.get("score", 0.0) + 0.01 * overlap)
    return sorted(items, key=lambda x: x["score"], reverse=True)
