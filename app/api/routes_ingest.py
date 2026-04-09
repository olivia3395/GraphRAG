from fastapi import APIRouter, HTTPException
from app.core.schema import IngestRequest

router = APIRouter()
pipeline_ref = {}


def set_ingestion_pipeline(pipeline):
    pipeline_ref["pipeline"] = pipeline


@router.post("/ingest")
def ingest(req: IngestRequest):
    if "pipeline" not in pipeline_ref:
        raise HTTPException(status_code=500, detail="Ingestion pipeline not initialized")
    try:
        result = pipeline_ref["pipeline"].ingest(req.data_dir)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"message": "ingestion complete", **result}
