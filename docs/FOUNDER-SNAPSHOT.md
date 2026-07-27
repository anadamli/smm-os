# Founder snapshot — SMM OS (Ana MVP)

**Updated:** 2026-07-27 · **Read time:** ~2 minutes

This repo tracks **product engineering** for Ana's thin SMM assistant. Client content drafts, brand packs, and operator workflows stay on Ana's machine and are **not** pushed here.

---

## What this is

A **personal operator tool** (not the full 28-agent `AiFinPay-smm` farm): ingest brand canon → search with citations → (next) grounded drafts with QC → export approval packs. Human approval before anything goes live.

**Scope canon:** [SOW.md](../SOW.md)  
**Build plan:** [PLAN-MVP.md](./PLAN-MVP.md) · [TODO-MVP.md](./TODO-MVP.md)

---

## What shipped (GitHub)

| Milestone | Status | Evidence |
|-----------|--------|----------|
| Planning & alignment | Done (2026-07-24) | SOW, gap analysis, MVP plan; @pironmind confirmed thin tool in this repo |
| **Slice 1 — Knowledge** | **Done** (2026-07-24) | Brand ingest script, `/v1/search`, retrieval eval (`scripts/`, `eval/`) |
| Slice 2 — Draft + QC | Next | `POST /v1/drafts` not started |
| Slice 3 — Export | Planned | Template export to approval packs |
| Dashboard / agents | Deferred | See Phase 0 docs for long-term reference only |

---

## What is local only (not in this repo)

- Social post drafts, Wave 1 publish packs, designer handoffs
- `knowledge/brand-pack-v1.md` and client sources (ingested locally via env path)
- Operator inbox, decision logs, founder chat exports

Ana runs content ops in parallel; progress there does not appear in git history.

---

## Architecture note (one paragraph)

**Now:** Qdrant indexes brand text for grounded retrieval; drafts still live in markdown locally.  
**Later:** Supabase/Postgres becomes system of record for drafts and approvals (see PLAN-MVP §9 scale ladder). This MVP is a strangler toward the org's `AiFinPay-smm` reference — not a throwaway prototype.

---

## Read first

1. **[SOW.md](../SOW.md)** — what we build now vs what we explicitly skip  
2. **[PLAN-MVP.md](./PLAN-MVP.md)** — three build slices + scale path  
3. **`apps/api/README.md`** — run the API and Slice 1 ingest/eval locally  

Questions Q1–Q7 in PLAN-MVP §7 remain open where noted; alignment on repo strategy (thin tool here) is settled.
