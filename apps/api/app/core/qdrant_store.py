from typing import Dict, List, Optional
from uuid import uuid4

from qdrant_client import QdrantClient
from qdrant_client.http import models as qm

from app.core.config import get_settings


def get_qdrant() -> QdrantClient:
    settings = get_settings()
    if not settings.qdrant_url or not settings.qdrant_api_key:
        raise RuntimeError("QDRANT_URL / QDRANT_API_KEY missing in .env")
    return QdrantClient(
        url=settings.qdrant_url,
        api_key=settings.qdrant_api_key,
        check_compatibility=False,
    )


def ensure_collection() -> None:
    settings = get_settings()
    client = get_qdrant()
    name = settings.qdrant_collection
    if not client.collection_exists(name):
        client.create_collection(
            collection_name=name,
            vectors_config=qm.VectorParams(
                size=settings.embedding_dim,
                distance=qm.Distance.COSINE,
            ),
        )

    # Cloud Qdrant requires indexes for filtered fields
    for field in ("workspace_id", "partition", "document_id"):
        try:
            client.create_payload_index(
                collection_name=name,
                field_name=field,
                field_schema=qm.PayloadSchemaType.KEYWORD,
            )
        except Exception:
            # already exists
            pass


def upsert_chunks(
    workspace_id: str,
    document_id: str,
    title: str,
    partition: str,
    chunks: List[str],
    vectors: List[List[float]],
) -> List[str]:
    if len(chunks) != len(vectors):
        raise ValueError("chunks and vectors length mismatch")

    settings = get_settings()
    client = get_qdrant()
    ensure_collection()

    point_ids: List[str] = []
    points = []
    for i, (text, vector) in enumerate(zip(chunks, vectors)):
        pid = str(uuid4())
        point_ids.append(pid)
        points.append(
            qm.PointStruct(
                id=pid,
                vector=vector,
                payload={
                    "workspace_id": workspace_id,
                    "document_id": document_id,
                    "chunk_index": i,
                    "title": title,
                    "partition": partition,
                    "text": text,
                },
            )
        )

    client.upsert(collection_name=settings.qdrant_collection, points=points)
    return point_ids


def search(
    workspace_id: str,
    query_vector: List[float],
    top_k: int = 5,
    partition: Optional[str] = None,
) -> List[Dict]:
    settings = get_settings()
    client = get_qdrant()
    ensure_collection()

    must = [
        qm.FieldCondition(
            key="workspace_id",
            match=qm.MatchValue(value=workspace_id),
        )
    ]
    if partition:
        must.append(
            qm.FieldCondition(
                key="partition",
                match=qm.MatchValue(value=partition),
            )
        )

    results = client.query_points(
        collection_name=settings.qdrant_collection,
        query=query_vector,
        limit=top_k,
        query_filter=qm.Filter(must=must),
        with_payload=True,
    )

    hits: List[Dict] = []
    for r in results.points:
        payload = r.payload or {}
        hits.append(
            {
                "score": r.score,
                "title": payload.get("title"),
                "partition": payload.get("partition"),
                "text": payload.get("text"),
                "document_id": payload.get("document_id"),
                "chunk_index": payload.get("chunk_index"),
            }
        )
    return hits
