from typing import Dict, Any


class MetadataStore:
    def __init__(self):
        self._data: Dict[str, Dict[str, Any]] = {}

    def set(self, key: str, value: Dict[str, Any]) -> None:
        self._data[key] = value

    def get(self, key: str):
        return self._data.get(key)
