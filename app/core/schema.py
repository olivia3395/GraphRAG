from pydantic import BaseModel, Field
from typing import List, Dict, Any


class IngestRequest(BaseModel):
    data_dir: str = Field(..., description="Path to a local directory containing text and image files")


class QueryRequest(BaseModel):
    question: str
    top_k_text: int = 5
    top_k_image: int = 3
    graph_hops: int = 1
    use_multimodal: bool = True


class RetrievedItem(BaseModel):
    id: str
    score: float
    content: str
    metadata: Dict[str, Any]


class QueryResponse(BaseModel):
    answer: str
    text_evidence: List[RetrievedItem]
    image_evidence: List[RetrievedItem]
    expanded_nodes: List[str]
