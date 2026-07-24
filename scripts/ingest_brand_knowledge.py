#!/usr/bin/env python3
"""Ingest local brand-pack + social-voice into Qdrant via the knowledge service.

Runs from repo root or apps/api. Does not commit knowledge files.
Usage:
  cd apps/api && source .venv/bin/activate
  python ../../scripts/ingest_brand_knowledge.py
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
API_ROOT = REPO_ROOT / "apps" / "api"
DEFAULT_FILES = [
    REPO_ROOT / "knowledge" / "brand-pack-v1.md",
    REPO_ROOT / "knowledge" / "social-voice-v1.md",
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Ingest AiFinPay brand markdown into Qdrant")
    parser.add_argument(
        "--files",
        nargs="*",
        type=Path,
        default=DEFAULT_FILES,
        help="Markdown files to ingest (default: brand-pack + social-voice)",
    )
    args = parser.parse_args()

    sys.path.insert(0, str(API_ROOT))
    # Load apps/api/.env
    import os

    os.chdir(API_ROOT)

    from app.core import qdrant_store
    from app.core.config import get_settings
    from app.core.embeddings import embed_texts
    from app.routers.knowledge import _chunk_text
    from uuid import uuid4

    settings = get_settings()
    workspace_id = settings.demo_workspace_id
    print(f"workspace_id={workspace_id}")
    print(f"collection={settings.qdrant_collection}")

    for path in args.files:
        path = path if path.is_absolute() else REPO_ROOT / path
        if not path.exists():
            print(f"SKIP missing: {path}")
            continue
        text = path.read_text(encoding="utf-8")
        if len(text.strip()) < 20:
            print(f"SKIP too short: {path}")
            continue
        title = path.stem
        partition = "brand" if "brand" in path.name else "voice"
        chunks = _chunk_text(text)
        print(f"Ingesting {path.name}: {len(chunks)} chunks…")
        vectors = embed_texts(chunks)
        document_id = str(uuid4())
        qdrant_store.upsert_chunks(
            workspace_id=workspace_id,
            document_id=document_id,
            title=title,
            partition=partition,
            chunks=chunks,
            vectors=vectors,
        )
        print(f"  OK document_id={document_id}")

    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
