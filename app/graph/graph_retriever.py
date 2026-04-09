from typing import List


class GraphRetriever:
    def __init__(self, graph_builder):
        self.graph_builder = graph_builder

    def expand_from_entities(self, entities: List[str], hops: int = 1) -> List[str]:
        expanded = set()
        for ent in entities:
            for node in self.graph_builder.neighbors(ent, hops=hops):
                expanded.add(node)
        return list(expanded)
