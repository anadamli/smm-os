#!/usr/bin/env python3
"""Check post text against brand guardrails — no Gemini/Qdrant needed.

Usage:
  python scripts/check_draft.py --text "Our ICP is TBD..."
  python scripts/check_draft.py --file operator/outbox/some-post.md
  pbpaste | python scripts/check_draft.py
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
API_ROOT = REPO_ROOT / "apps" / "api"


def main() -> int:
    parser = argparse.ArgumentParser(description="Check draft text against brand guardian")
    parser.add_argument("--text", help="Post text inline")
    parser.add_argument("--file", help="Path to a file containing the post text")
    args = parser.parse_args()

    if args.text:
        text = args.text
    elif args.file:
        text = Path(args.file).read_text(encoding="utf-8")
    else:
        text = sys.stdin.read()

    if not text.strip():
        print("ERROR: no text provided (use --text, --file, or pipe via stdin)", file=sys.stderr)
        return 1

    sys.path.insert(0, str(API_ROOT))

    from app.core.brand_guardian import score_draft

    result = score_draft(text)
    print(f"pass={result['pass']}")
    if result["flags"]:
        print("\nFLAGS:")
        for flag in result["flags"]:
            print(f"  [{flag['code']}] {flag['message']}")

    return 0 if result["pass"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
