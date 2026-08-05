from typing import List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services import drafts as draft_service

router = APIRouter(prefix="/v1", tags=["drafts"])


class DraftRequest(BaseModel):
    platform: str = Field(..., min_length=2, description="linkedin | instagram | x | threads")
    theme: str = Field(..., min_length=3)
    brief: str = ""
    workspace_id: Optional[str] = None
    top_k: int = Field(default=6, ge=1, le=20)


class Citation(BaseModel):
    id: str
    title: Optional[str] = None
    partition: Optional[str] = None
    document_id: Optional[str] = None
    chunk_index: Optional[int] = None
    score: Optional[float] = None
    excerpt: str


class ScorecardFlag(BaseModel):
    code: str
    message: str
    severity: str = "error"


class Scorecard(BaseModel):
    flags: List[ScorecardFlag]
    pass_: bool = Field(alias="pass")

    model_config = {"populate_by_name": True}


class DraftResponse(BaseModel):
    id: str
    platform: str
    theme: str
    brief: str
    workspace_id: str
    draft: str
    citations: List[Citation]
    scorecard: Scorecard
    pass_: bool = Field(alias="pass")

    model_config = {"populate_by_name": True}


def _to_response(record: dict) -> DraftResponse:
    sc = record["scorecard"]
    return DraftResponse(
        id=record["id"],
        platform=record["platform"],
        theme=record["theme"],
        brief=record["brief"],
        workspace_id=record["workspace_id"],
        draft=record["draft"],
        citations=record["citations"],
        scorecard=Scorecard(flags=sc["flags"], pass_=sc["pass"]),
        pass_=record["pass"],
    )


@router.post("/drafts", response_model=DraftResponse)
def create_draft(body: DraftRequest) -> DraftResponse:
    try:
        record = draft_service.create_draft(
            platform=body.platform,
            theme=body.theme,
            brief=body.brief,
            workspace_id=body.workspace_id,
            top_k=body.top_k,
        )
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return _to_response(record)


@router.get("/drafts/{draft_id}", response_model=DraftResponse)
def get_draft(draft_id: str) -> DraftResponse:
    record = draft_service.get_draft(draft_id)
    if not record:
        raise HTTPException(status_code=404, detail="Draft not found")
    return _to_response(record)
