# SMM OS

Commercial AI SMM Operating System — connect brand knowledge, ask grounded questions, draft on-brand posts, approve before anything goes live.

## Pilot promise

**Connect knowledge → ask about the product → get an on-brand draft → approve.**

## Status

| Area | State |
|------|--------|
| Product architecture | Done — see docs |
| Phase 0 plan | Active |
| FastAPI brain (`/health`, knowledge ingest/search) | Skeleton in progress |
| Dashboard (`apps/web`) | Not started |
| Agents (LangGraph) | After knowledge path is solid |

## Docs

- [Product architecture](docs/SMM-OS-PRODUCT-ARCHITECTURE.md) — canonical product north star
- [Phase 0 plan](docs/PHASE-0-PRODUCT.md) — what ships first

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
