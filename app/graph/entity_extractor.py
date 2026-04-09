import re
from typing import List


class SimpleEntityExtractor:
    """A lightweight heuristic extractor.

    It captures capitalized tokens and certain technical keywords.
    Replace with spaCy or LLM extraction for stronger performance.
    """

    def extract(self, text: str) -> List[str]:
        cap_words = re.findall(r"\b[A-Z][a-zA-Z0-9_-]{2,}\b", text)
        keywords = re.findall(r"\b(?:GraphRAG|RAG|CLIP|FastAPI|ChromaDB|retrieval|embedding|entity|graph|multimodal)\b", text, flags=re.IGNORECASE)
        entities = cap_words + [k.lower() for k in keywords]
        out = []
        seen = set()
        for item in entities:
            key = item.strip()
            if key and key not in seen:
                out.append(key)
                seen.add(key)
        return out[:15]
