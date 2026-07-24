#!/usr/bin/env python3
"""Run brand_questions.yaml against /v1/search (or direct Qdrant).

Usage (API must be optional — this uses services directly):
  cd apps/api && source .venv/bin/activate
  python ../../scripts/eval_brand_search.py
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
API_ROOT = REPO_ROOT / "apps" / "api"
EVAL_PATH = REPO_ROOT / "eval" / "brand_questions.yaml"


def main() -> int:
    sys.path.insert(0, str(API_ROOT))
    os.chdir(API_ROOT)

    from app.core.config import get_settings
    from app.core.embeddings import embed_query
    from app.core import qdrant_store

    data = yaml.safe_load(EVAL_PATH.read_text(encoding="utf-8"))
    questions = data["questions"]
    settings = get_settings()
    workspace_id = settings.demo_workspace_id

    passed = 0
    print(f"Evaluating {len(questions)} questions…\n")
    for q in questions:
        vector = embed_query(q["query"])
        hits = qdrant_store.search(
            workspace_id=workspace_id,
            query_vector=vector,
            top_k=5,
        )
        expect = q.get("expect_section", "")
        blob = " ".join((h.get("text") or "")[:500] for h in hits).lower()
        keywords = [k.lower() for k in q.get("keywords") or []]
        if not keywords:
            keywords = [
                t
                for t in expect.lower().replace("—", " ").replace("/", " ").split()
                if len(t) > 2
            ]
        ok = bool(hits) and any(k in blob for k in keywords)
        status = "PASS" if ok else "REVIEW"
        if ok:
            passed += 1
        top = (hits[0].get("text") or "")[:120].replace("\n", " ") if hits else "(no hits)"
        print(f"{q['id']} [{status}] expect={expect}")
        print(f"  Q: {q['query']}")
        print(f"  top: {top}…\n")

    print(f"Result: {passed}/{len(questions)} heuristic pass")
    print("Manual: open hits and confirm they match brand-pack sections (pass_rule in yaml).")
    return 0 if passed >= 7 else 1


if __name__ == "__main__":
    raise SystemExit(main())
