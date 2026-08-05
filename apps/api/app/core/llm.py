"""Text generation via Gemini (Slice 2 drafts)."""

from __future__ import annotations

from google import genai

from app.core.config import get_settings


def generate_text(prompt: str, *, system: str | None = None) -> str:
    settings = get_settings()
    if not settings.gemini_api_key:
        raise RuntimeError("GEMINI_API_KEY is missing in apps/api/.env")

    client = genai.Client(api_key=settings.gemini_api_key)
    config = None
    if system:
        config = {"system_instruction": system}

    response = client.models.generate_content(
        model=settings.llm_model,
        contents=prompt,
        config=config,
    )

    text = (response.text or "").strip()
    if not text:
        raise RuntimeError("LLM returned empty draft")
    return text
