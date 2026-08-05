"""Draft generation: retrieval + LLM + brand guardian (Slice 2)."""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from uuid import uuid4

from app.core import qdrant_store
from app.core.brand_guardian import score_draft
from app.core.config import get_settings
from app.core.embeddings import embed_query
from app.core.llm import generate_text

_draft_store: Dict[str, Dict[str, Any]] = {}

PLATFORM_GUIDANCE: Dict[str, str] = {
    "linkedin": (
        "LinkedIn: long-form builder narrative (roughly 150–400 words unless brief asks shorter). "
        "One clear idea, bullet mechanics OK, soft CTA at end."
    ),
    "instagram": (
        "Instagram: short caption (roughly 3–8 lines), punchy, visual-first; minimal hashtags unless brief says."
    ),
    "x": (
        "X/Twitter: one tight post (under 280 chars if possible); hook first; one CTA link optional."
    ),
    "threads": (
        "Threads: conversational builder tone, same claim discipline as X, slightly longer OK."
    ),
}

SYSTEM_INSTRUCTION = """You write on-brand social posts for AiFinPay.
Rules:
- Use ONLY facts from the provided BRAND CONTEXT. Do not invent customers, revenue, or metrics.
- CTA domain: https://aifinpay.io only (no .com / .company).
- Tone: precise, builder-first, mechanics over hype.
- If a required fact is missing from context, write the literal token TBD — do not guess.
- Output post body only — no titles, no markdown headers, no meta commentary."""


def _build_retrieval_query(theme: str, brief: str) -> str:
    parts = [theme.strip()]
    if brief.strip():
        parts.append(brief.strip())
    return " ".join(parts)


def _format_context(hits: List[Dict[str, Any]]) -> tuple[str, List[Dict[str, Any]]]:
    citations: List[Dict[str, Any]] = []
    blocks: List[str] = []
    for i, hit in enumerate(hits, start=1):
        text = (hit.get("text") or "").strip()
        if not text:
            continue
        label = hit.get("title") or "brand-pack"
        partition = hit.get("partition") or ""
        cite_id = f"c{i}"
        citations.append(
            {
                "id": cite_id,
                "title": label,
                "partition": partition,
                "document_id": hit.get("document_id"),
                "chunk_index": hit.get("chunk_index"),
                "score": hit.get("score"),
                "excerpt": text[:400],
            }
        )
        blocks.append(f"[{cite_id}] ({label} / {partition})\n{text}")
    return "\n\n---\n\n".join(blocks), citations


def _build_prompt(
    platform: str,
    theme: str,
    brief: str,
    context: str,
) -> str:
    platform_key = platform.lower()
    guidance = PLATFORM_GUIDANCE.get(
        platform_key,
        "Match the platform's native format and length.",
    )
    return f"""Platform: {platform}
Theme: {theme}
Brief: {brief}

Platform craft:
{guidance}

BRAND CONTEXT (cite mentally; do not output citation markers):
{context}

Write the post now."""


def create_draft(
    *,
    platform: str,
    theme: str,
    brief: str = "",
    workspace_id: Optional[str] = None,
    top_k: int = 6,
) -> Dict[str, Any]:
    settings = get_settings()
    ws = workspace_id or settings.demo_workspace_id
    query = _build_retrieval_query(theme, brief)

    vector = embed_query(query)
    hits = qdrant_store.search(workspace_id=ws, query_vector=vector, top_k=top_k)
    context, citations = _format_context(hits)
    if not context:
        raise RuntimeError(
            "No brand context retrieved. Run scripts/ingest_brand_knowledge.py first."
        )

    prompt = _build_prompt(platform, theme, brief, context)
    draft_text = generate_text(prompt, system=SYSTEM_INSTRUCTION)
    scorecard = score_draft(draft_text)

    draft_id = str(uuid4())
    record = {
        "id": draft_id,
        "platform": platform,
        "theme": theme,
        "brief": brief,
        "workspace_id": ws,
        "draft": draft_text,
        "citations": citations,
        "scorecard": scorecard,
        "pass": scorecard["pass"],
    }
    _draft_store[draft_id] = record
    return record


def get_draft(draft_id: str) -> Optional[Dict[str, Any]]:
    return _draft_store.get(draft_id)
