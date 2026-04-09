import networkx as nx
from typing import List, Dict


class KnowledgeGraphBuilder:
    def __init__(self):
        self.graph = nx.Graph()

    def add_chunk_entities(self, chunk_id: str, entities: List[str], metadata: Dict):
        self.graph.add_node(chunk_id, node_type="chunk", **metadata)
        for ent in entities:
            self.graph.add_node(ent, node_type="entity")
            self.graph.add_edge(chunk_id, ent, relation="mentions")

    def connect_cooccurring_entities(self, entities: List[str]):
        for i in range(len(entities)):
            for j in range(i + 1, len(entities)):
                u, v = entities[i], entities[j]
                if self.graph.has_edge(u, v):
                    self.graph[u][v]["weight"] = self.graph[u][v].get("weight", 1) + 1
                else:
                    self.graph.add_edge(u, v, relation="cooccurs", weight=1)

    def neighbors(self, node: str, hops: int = 1):
        if node not in self.graph:
            return []
        visited = {node}
        frontier = {node}
        for _ in range(hops):
            next_frontier = set()
            for current in frontier:
                next_frontier.update(self.graph.neighbors(current))
            frontier = next_frontier - visited
            visited.update(frontier)
        visited.discard(node)
        return list(visited)

    def clear(self):
        self.graph.clear()
