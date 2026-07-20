from typing import List, Optional
from uuid import uuid4

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.core import qdrant_store
from app.core.config import get_settings
from app.core.embeddings import embed_query, embed_texts

router = APIRouter(prefix="/v1", tags=["knowledge"])


class IngestTextRequest(BaseModel):
    title: str = Field(..., min_length=1)
    text: str = Field(..., min_length=20)
    partition: str = "other"
    workspace_id: Optional[str] = None


class IngestTextResponse(BaseModel):
    document_id: str
    chunks: int
    workspace_id: str


class SearchRequest(BaseModel):
    query: str = Field(..., min_length=2)
    top_k: int = Field(default=5, ge=1, le=20)
    partition: Optional[str] = None
    workspace_id: Optional[str] = None


def _chunk_text(text: str, max_chars: int = 1200) -> List[str]:
    parts = [p.strip() for p in text.split("\n\n") if p.strip()]
    if not parts:
        parts = [text.strip()]

    chunks: List[str] = []
    buf = ""
    for part in parts:
        if not buf:
            buf = part
        elif len(buf) + 2 + len(part) <= max_chars:
            buf = "{}\n\n{}".format(buf, part)
        else:
            chunks.append(buf)
            buf = part
    if buf:
        chunks.append(buf)
    return chunks


@router.post("/ingest/text", response_model=IngestTextResponse)
def ingest_text(body: IngestTextRequest) -> IngestTextResponse:
    settings = get_settings()
    workspace_id = body.workspace_id or settings.demo_workspace_id
    document_id = str(uuid4())
    chunks = _chunk_text(body.text)

    try:
        vectors = embed_texts(chunks)
        qdrant_store.upsert_chunks(
            workspace_id=workspace_id,
            document_id=document_id,
            title=body.title,
            partition=body.partition,
            chunks=chunks,
            vectors=vectors,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return IngestTextResponse(
        document_id=document_id,
        chunks=len(chunks),
        workspace_id=workspace_id,
    )


@router.post("/search")
def search(body: SearchRequest) -> dict:
    settings = get_settings()
    workspace_id = body.workspace_id or settings.demo_workspace_id

    try:
        vector = embed_query(body.query)
        hits = qdrant_store.search(
            workspace_id=workspace_id,
            query_vector=vector,
            top_k=body.top_k,
            partition=body.partition,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return {"query": body.query, "workspace_id": workspace_id, "hits": hits}
