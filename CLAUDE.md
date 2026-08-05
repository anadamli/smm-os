# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Start here

Read [AGENTS.md](AGENTS.md) first — it defines scope boundaries (this is a thin FastAPI
tool, not a multi-agent platform), the product-dev vs client-ops track split, and
conventions. This file adds commands and architecture detail for the `apps/api` code.

## Commands

```bash
cd apps/api
python3 -m venv .venv && source .venv/bin/activate   # first time only
pip install -r requirements.txt

cp ../../.env.example .env   # fill GEMINI_API_KEY, QDRANT_URL, QDRANT_API_KEY at minimum

uvicorn app.main:app --reload --port 8000   # run API — health: /health, docs: /docs
pytest tests/ -q                             # run tests (no API keys required)
pytest tests/test_brand_guardian.py -q       # run a single test file
pytest tests/test_brand_guardian.py::test_tbd_fails -q   # run a single test
```

Ingest and eval (from `apps/api`, venv active; brand files live in gitignored `knowledge/` at repo root):

```bash
python ../../scripts/ingest_brand_knowledge.py   # embeds + upserts knowledge/*.md into Qdrant
python ../../scripts/eval_brand_search.py        # runs eval/brand_questions.yaml against /v1/search
python ../../scripts/draft_post.py --platform linkedin --theme "..." --brief "..."   # CLI draft + QC; exit 0=pass, 2=flags present
```

There is no lint/format command configured yet.

## Architecture

Two-slice pipeline, both slices require Qdrant to be reachable and populated (ingest
before search/drafts):

```
knowledge/*.md --[ingest_brand_knowledge.py]--> chunk --> embed (Gemini) --> Qdrant upsert
                                                                                   |
user query/theme --[embed_query]--> Qdrant search (filtered by workspace_id) -----'
                                                                                   |
                                                              draft: LLM generate_text()
                                                                     -> brand_guardian.score_draft()
                                                                     -> {draft, citations[], scorecard}
```

- `app/core/config.py` — `Settings` (pydantic-settings, reads `apps/api/.env`). All
  external config (Qdrant, Gemini, workspace id) flows through `get_settings()`
  (`@lru_cache`), never read env vars directly elsewhere.
- `app/core/embeddings.py` — Gemini embeddings only (`embedding_model` /
  `embedding_dim` in Settings must match — the client raises if the model's returned
  dim differs from configured).
- `app/core/qdrant_store.py` — all Qdrant I/O. Every point is scoped by
  `workspace_id` payload field; `search()` always filters on it. Collection is
  lazily created/indexed via `ensure_collection()` on first use.
- `app/core/llm.py` — Gemini text generation (`generate_text`), used only by the
  draft service.
- `app/core/brand_guardian.py` — pure rule-based checks (banned phrases, URL
  allowlist, TBD leakage) over generated text; no network calls. `score_draft()`
  returns `{flags[], pass}`; `pass` is false if any flag has `severity == "error"`.
  This is a *subset* of brand-pack §9 guardrails — extend the tuples here as the
  brand pack evolves, don't add a second mechanism.
- `app/routers/` — thin HTTP layer (`knowledge.py` = `/v1/search`, `/v1/ingest/text`;
  `drafts.py` = `/v1/drafts`). Business logic for drafts lives in
  `app/services/drafts.py`, not the router.
- `app/services/drafts.py` — orchestrates retrieval -> prompt build -> LLM ->
  brand guardian -> in-memory `_draft_store` (no persistence yet — Slice 3, see
  `docs/TODO-MVP.md` Phase 3). `PLATFORM_GUIDANCE` and `SYSTEM_INSTRUCTION` here
  encode the per-platform tone rules; change them here, not in the router.

**Workspace model** ([ADR 001](docs/adr/001-single-workspace-local-mvp.md)): single
demo workspace (`Settings.demo_workspace_id`), no auth. Local-only, do not expose
publicly. Every Qdrant read/write must still pass `workspace_id` explicitly —
don't rely on it being the only tenant as an excuse to drop the filter.

`docs/TODO-MVP.md` is the sequential build list — check current phase/slice before
starting new work. `docs/adr/` holds accepted architecture decisions.
