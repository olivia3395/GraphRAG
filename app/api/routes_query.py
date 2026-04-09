from fastapi import APIRouter, HTTPException
from app.core.schema import QueryRequest

router = APIRouter()
answer_ref = {}


def set_answer_pipeline(pipeline):
    answer_ref["pipeline"] = pipeline


@router.post("/query")
def query(req: QueryRequest):
    if "pipeline" not in answer_ref:
        raise HTTPException(status_code=500, detail="Answer pipeline not initialized")
    try:
        return answer_ref["pipeline"].answer(
            question=req.question,
            top_k_text=req.top_k_text,
            top_k_image=req.top_k_image,
            graph_hops=req.graph_hops,
            use_multimodal=req.use_multimodal,
        )
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
