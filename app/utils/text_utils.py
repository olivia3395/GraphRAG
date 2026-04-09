import re
from typing import List


def normalize_whitespace(text: str) -> str:
    return " ".join(text.split())


def split_sentences(text: str) -> List[str]:
    text = normalize_whitespace(text)
    parts = re.split(r"(?<=[.!?])\s+", text)
    return [p.strip() for p in parts if p.strip()]
