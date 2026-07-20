from typing import List

from google import genai

from app.core.config import get_settings


def embed_texts(texts: List[str]) -> List[List[float]]:
    """Embed strings with Gemini. Returns one vector per input text."""
    settings = get_settings()
    if not settings.gemini_api_key:
        raise RuntimeError("GEMINI_API_KEY is missing in apps/api/.env")

    client = genai.Client(api_key=settings.gemini_api_key)
    vectors: List[List[float]] = []

    for text in texts:
        result = client.models.embed_content(
            model=settings.embedding_model,
            contents=text,
        )
        emb = result.embeddings[0]
        values = list(emb.values)
        if len(values) != settings.embedding_dim:
            raise RuntimeError(
                "Embedding dim {} != configured {}. "
                "Update embedding_dim in config if the model changed.".format(
                    len(values), settings.embedding_dim
                )
            )
        vectors.append(values)

    return vectors


def embed_query(text: str) -> List[float]:
    return embed_texts([text])[0]
