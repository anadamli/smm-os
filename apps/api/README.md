# SMM OS API

Thin FastAPI brain for Ana's MVP: ingest brand knowledge → search with citations → grounded drafts + QC.

## Setup

```bash
cd apps/api
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp ../../.env.example .env   # or copy existing apps/api/.env
# Fill at least: GEMINI_API_KEY, QDRANT_URL, QDRANT_API_KEY
```

## Run API

```bash
cd apps/api
source .venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

- Health: http://127.0.0.1:8000/health
- OpenAPI: http://127.0.0.1:8000/docs

## Slice 1 — ingest brand-pack (local only)

Brand files live in gitignored `knowledge/` at repo root. Ingest does **not** commit them.

```bash
cd apps/api
source .venv/bin/activate
python ../../scripts/ingest_brand_knowledge.py
python ../../scripts/eval_brand_search.py
```

Eval cases: `eval/brand_questions.yaml` (pass ≈ 7/10 with relevant citations).

Manual search via API:

```bash
curl -s http://127.0.0.1:8000/v1/search \
  -H 'content-type: application/json' \
  -d '{"query":"Who is our ICP?","top_k":5}'
```

## Slice 2 — grounded draft + brand QC

Requires Slice 1 ingest first (Qdrant populated).

**CLI (recommended):**

```bash
cd apps/api
source .venv/bin/activate
python ../../scripts/draft_post.py \
  --platform linkedin \
  --theme "card on file is hidden human in every agent" \
  --brief "Problem framing LI-1; CTA aifinpay.io; multichain x12"
```

Exit code `0` = QC pass, `2` = draft generated but flags present.

**API:**

```bash
curl -s http://127.0.0.1:8000/v1/drafts \
  -H 'content-type: application/json' \
  -d '{
    "platform": "linkedin",
    "theme": "card on file is hidden human in every agent",
    "brief": "Problem framing LI-1"
  }' | jq .
```

Response shape: `{ id, draft, citations[], scorecard: { flags[], pass }, pass }`.

Retrieve by id: `GET /v1/drafts/{id}` (in-memory until Slice 3 persistence).

**Tests (no API keys):**

```bash
cd apps/api && source .venv/bin/activate && pytest tests/ -q
```

## Workspace model

See [ADR 001](../../docs/adr/001-single-workspace-local-mvp.md): single local workspace, no auth yet.
