# SMM OS

Commercial AI SMM Operating System — connect brand knowledge, ask grounded questions, draft on-brand posts, approve before anything goes live.

## Pilot promise

**Connect knowledge → ask about the product → get an on-brand draft → approve.**

## For founders (2 min)

Start with **[docs/FOUNDER-SNAPSHOT.md](docs/FOUNDER-SNAPSHOT.md)** — what shipped, what's next, what stays local.  
Scope: **[SOW.md](SOW.md)**.

## Status

*Last updated: 2026-07-27*

| Area | State |
|------|--------|
| **MVP scope** | **Active — [SOW.md](SOW.md)** |
| Planning & alignment | Done (2026-07-24) — thin tool in this repo confirmed with dev |
| MVP plan & tasks | [PLAN-MVP.md](docs/PLAN-MVP.md) · [TODO-MVP.md](docs/TODO-MVP.md) · [GAP-ANALYSIS.md](docs/GAP-ANALYSIS.md) |
| **Slice 1 — Knowledge** | **Done** — ingest script, `/v1/search`, retrieval eval |
| **Slice 2 — Draft + QC** | **Next** — `POST /v1/drafts` |
| Slice 3 — Export | Planned |
| Product architecture (long-term) | Reference — [docs/SMM-OS-PRODUCT-ARCHITECTURE.md](docs/SMM-OS-PRODUCT-ARCHITECTURE.md) |
| Phase 0 full SaaS | Deferred — [docs/PHASE-0-PRODUCT.md](docs/PHASE-0-PRODUCT.md) |
| Dashboard (`apps/web`) | Not started |
| Agents (LangGraph) | Deferred — thin draft pipeline first |
| Client content / Wave posts | **Local ops only** — not in this repo |

## Docs

One product story:

- **[SOW.md](SOW.md)** — Ana MVP scope (what we build now)
- [Founder snapshot](docs/FOUNDER-SNAPSHOT.md) — quick status for review
- [MVP plan](docs/PLAN-MVP.md) — architecture + build slices
- [Product architecture](docs/SMM-OS-PRODUCT-ARCHITECTURE.md) — long-term north star
- [Phase 0 plan](docs/PHASE-0-PRODUCT.md) — full SaaS reference (trimmed for MVP)

## Layout

```
apps/api    — FastAPI backend (brain)
apps/web    — Next.js dashboard (later)
supabase/   — DB migrations + RLS (deferred for MVP)
scripts/    — ingest + eval CLI
eval/       — retrieval eval sets
fixtures/   — safe demo brand (not real clients)
docs/       — product docs
```

## Local setup

1. Copy `.env.example` → `apps/api/.env` and fill values (never commit secrets).
2. See `apps/api/README.md` for running the API and Slice 1 ingest/eval.

## What this repo is (and is not)

This repository tracks **product progress** for founders and future engineering. Client ops, brand packs, and private working notes stay local and are not pushed here.
