from app.graph.graph_builder import KnowledgeGraphBuilder


def test_graph_builder_adds_nodes_and_edges():
    gb = KnowledgeGraphBuilder()
    gb.add_chunk_entities("chunk_1", ["Boston", "Harvard"], {"content": "..."})
    assert "chunk_1" in gb.graph.nodes
    assert "Boston" in gb.graph.nodes
    assert gb.graph.has_edge("chunk_1", "Boston")
