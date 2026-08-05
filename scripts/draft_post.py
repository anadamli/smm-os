#!/usr/bin/env python3
"""Generate a grounded social draft via Slice 2 API services.

Usage:
  cd apps/api && source .venv/bin/activate
  python ../../scripts/draft_post.py --platform linkedin --theme "card on file problem"
  python ../../scripts/draft_post.py --platform linkedin --theme "LI-1" \\
    --brief "Problem framing: card on file is hidden human in every agent"
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
API_ROOT = REPO_ROOT / "apps" / "api"


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate brand-grounded post draft")
    parser.add_argument(
        "--platform",
        required=True,
        choices=["linkedin", "instagram", "x", "threads"],
        help="Target platform",
    )
    parser.add_argument("--theme", required=True, help="Post theme / rubric")
    parser.add_argument("--brief", default="", help="Optional extra brief")
    parser.add_argument("--json", action="store_true", help="Print full JSON response")
    args = parser.parse_args()

    sys.path.insert(0, str(API_ROOT))
    os.chdir(API_ROOT)

    from app.services.drafts import create_draft

    try:
        record = create_draft(
            platform=args.platform,
            theme=args.theme,
            brief=args.brief,
        )
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(record, indent=2, ensure_ascii=False))
    else:
        print(f"draft_id={record['id']}")
        print(f"pass={record['pass']}")
        print(f"citations={len(record['citations'])}")
        if record["scorecard"]["flags"]:
            print("\nFLAGS:")
            for flag in record["scorecard"]["flags"]:
                print(f"  [{flag['code']}] {flag['message']}")
        print("\n--- DRAFT ---\n")
        print(record["draft"])

    return 0 if record["pass"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
