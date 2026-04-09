from app.retrieval.reranker import simple_rerank


def test_simple_rerank_keeps_items():
    items = [
        {"id": "1", "score": 0.2, "content": "graph retrieval and entity expansion"},
        {"id": "2", "score": 0.3, "content": "image retrieval pipeline"},
    ]
    ranked = simple_rerank("graph retrieval", items)
    assert len(ranked) == 2
    assert ranked[0]["id"] == "1"
