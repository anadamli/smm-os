# ADR 001 — Single workspace, no auth (local MVP)

- **Status:** Accepted
- **Date:** 2026-07-24
- **Context:** Ana MVP is a personal time-saving tool for one brand (AiFinPay), not multi-tenant SaaS. Full Phase 0 planned JWT + RLS; that slows Slice 1.

## Decision

1. **One workspace** identified by `DEMO_WORKSPACE_ID` / `Settings.demo_workspace_id` (UUID string in env).
2. **No auth** on local API for MVP — bind to localhost; do not expose publicly.
3. Operator brand files stay under local `knowledge/` (gitignored); ingest via script/API, never commit client pack.

## Consequences

- Fast path to searchable brand-pack and grounded drafts.
- Must add auth before any shared deploy or second client.
- Matches SOW Option A (thin tool).

## Alternatives considered

- Supabase Auth + RLS now — deferred (SOW out of scope).
- Fork AiFinPay-smm tenancy — rejected for MVP size.
