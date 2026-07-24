# SMM OS

Commercial AI SMM Operating System — connect brand knowledge, ask grounded questions, draft on-brand posts, approve before anything goes live.

## Pilot promise

**Connect knowledge → ask about the product → get an on-brand draft → approve.**

## Status

| Area | State |
|------|--------|
| **MVP scope (operator tool)** | **Active — [SOW.md](SOW.md)** |
| MVP plan & tasks | [PLAN-MVP.md](docs/PLAN-MVP.md) · [TODO-MVP.md](docs/TODO-MVP.md) · [GAP-ANALYSIS.md](docs/GAP-ANALYSIS.md) |
| Product architecture (long-term) | Done — see docs |
| Phase 0 plan (full SaaS — deferred) | Reference only |
| FastAPI brain (`/health`, knowledge ingest/search) | **Slice 1 live** — brand ingest + eval scripts |
| Dashboard (`apps/web`) | Not started |
| Agents (LangGraph) | Deferred — thin draft pipeline first |

## Docs

One product story — start here:

- **[SOW.md](SOW.md)** — Ana MVP scope (what we build now)
- [MVP plan](docs/PLAN-MVP.md) — architecture + build slices
- [Product architecture](docs/SMM-OS-PRODUCT-ARCHITECTURE.md) — long-term north star
- [Phase 0 plan](docs/PHASE-0-PRODUCT.md) — full SaaS reference (trimmed for MVP)

## Layout

```
apps/api    — FastAPI backend (brain)
apps/web    — Next.js dashboard (later)
supabase/   — DB migrations + RLS
n8n/        — integration workflows only
eval/       — retrieval / agent eval sets
fixtures/   — safe demo brand (not real clients)
docs/       — product docs
```

## Local setup

1. Copy `.env.example` → `apps/api/.env` and fill values (never commit secrets).
2. See `apps/api/README.md` for running the API.

## What this repo is (and is not)

This repository tracks **product progress** for founders and future engineering. Client ops, brand packs, and private working notes stay local and are not pushed here.
