# Gap Analysis — AiFinPay-smm vs Local smm OS vs Ana Operator Reality

> **Purpose:** Decide what to keep, drop, or defer for Ana's MVP.  
> **Sources:** cloned `AiFinPay-smm` (local path), Ana's `smm OS` repo, `operator/` + `knowledge/` workflow.  
> **Not used:** empty smart-contracts Google Sheet.

---

## Executive summary

| Layer | Verdict |
|-------|---------|
| **Ana operator files** | **Keep** — source of truth for workflow until tool replaces each file |
| **Local `smm OS` API skeleton** | **Keep & extend** — right size for MVP |
| **`AiFinPay-smm` full stack** | **Reference only** — do not fork; cherry-pick patterns/tests later |
| **Phase 0 / Architecture docs** | **Trim** — tenancy, 5-node LangGraph, Vercel UI → defer |

---

## Comparison table

| Feature / capability | AiFinPay-smm (founder repo) | Local smm OS | Ana operator today | Needed for Ana MVP | Verdict |
|----------------------|----------------------------|--------------|-------------------|-------------------|---------|
| **Brand canon source** | `fixtures/aifinpay-brand.md` (demo) | `fixtures/demo-brand.md` | `knowledge/brand-pack-v1.md` (local, filled) | Yes — ingest local brand-pack | **Keep** (operator canon); **drop** demo fixture as prod source |
| **Markdown/PDF ingest** | Full: PDF, DOCX, CSV, JSON, URL, dedup, versions | `/v1/ingest/text` only | Manual copy into content-plan | Yes — start with MD ingest | **Keep** (extend local); **defer** URL/Drive |
| **Vector search (Qdrant)** | Yes + lexical fallback | Yes (basic) | N/A (Cursor reads files) | Yes | **Keep** local skeleton |
| **Grounded draft generation** | 28 roles, channel-native, orchestrator | Not built | Cursor + `brand-grounded-copy` skill | Yes — single draft endpoint | **Keep** (build thin); **drop** 28 agents |
| **Brand / claim check** | brand_review + compliance_review stages | Not built | Manual QC in skill + eye | Yes — automated flags | **Keep** (build); **reference** AiFinPay checks |
| **Human approval (HITL)** | Two gates: plan + content; DB + UI | Not built | `post-for-approval.md`, `decision-log.md` | Yes — export to templates | **Keep** (markdown first); **defer** full UI |
| **Content plan / calendar** | Autopilot generates plans | Not built | `content-plan-14d.md` (20 drafts) | Yes — helper only | **Keep** (operator file); **drop** autopilot |
| **Visual handoff** | Channel previews, media gen at publish | Not built | `image-prompt-pack.md` + `visuals/{id}/` | Yes — export prompts | **Keep** (template export) |
| **Founder inbox / decisions** | Obsidian memory, audit events | Not built | `founder-inbox.md`, `decision-log.md` | Yes — manual for MVP | **Keep** (files); **defer** TG webhook |
| **Publish to social** | Postiz, Telegram, Discord, dry_run/live | Not built | No access; ⏸ paused | No | **Drop** for MVP |
| **21 channel contracts** | Full catalog | Not built | LI, IG, X, Threads in plan | Partial — 4 platforms in content-plan | **Defer** extra channels |
| **Web live research** | Tavily/Serper/Brave | Not built | Not used | No | **Drop** for MVP |
| **Autopilot / Celery scheduler** | Beat cycles, blocks on pending approval | Not built | Ana-driven cadence | No | **Drop** |
| **Analytics / weekly reports** | Full metrics, cost models | Not built | `metrics-weekly.md` manual | No | **Defer** |
| **Multi-tenant auth (JWT/RBAC)** | Complete | Planned in Phase 0 | Single operator | No for MVP | **Defer** |
| **Supabase + RLS schema** | PostgreSQL + Alembic (in org repo) | Migration sketch in docs only | N/A | No for MVP | **Defer** |
| **Next.js dashboard** | Working operator UI | `.gitkeep` only | Uses Cursor + markdown | Optional later | **Defer** |
| **Docker Compose stack** | Full (api, web, worker, redis, postgres, qdrant) | Not present | Not needed locally yet | No for week 1 | **Defer** |
| **LangGraph agents** | 18-stage state machine | Planned 5-node | Cursor skills = "agents" | No — 1 pipeline script | **Drop** full graph for MVP |
| **Eval harness** | Tests + CI | `eval/retrieval.yaml` stub | Informal voice check | Yes — brand Q retrieval | **Keep** (extend local) |
| **Observability (Langfuse/Sentry)** | Wired | Not built | N/A | No for MVP | **Defer** |
| **n8n / Drive sync** | Documented | Mentioned in Phase 0 | Not used | No | **Defer** |
| **Social voice baseline** | In fixtures partially | Not in repo | `social-voice-v1.md` | Yes — ingest with brand-pack | **Keep** |
| **CTA domain rule** | Configurable | Not enforced | `aifinpay.io` only (founder 22.07) | Yes — hard check | **Keep** (implement in brand check) |
| **GitHub / founder visibility** | Org repo public-ish | Ana's product repo | Founder wants progress on GitHub | Yes — planning docs | **Keep** (push docs when asked) |

---

## Implementation maturity snapshot

| Repo | Lines of product code (approx.) | Runnable today | Ana can use without devops |
|------|--------------------------------|----------------|----------------------------|
| **AiFinPay-smm** | Large (API+web+worker+tests) | Yes, with Docker + keys | **No** — Postiz, LLM keys, ops |
| **smm OS (local)** | Small (~15 API files) | Partial — needs Qdrant + keys | **No** yet — **yes after Slice 1** |
| **operator/** | Markdown workflow | **Yes** — daily | **Yes** — current production |

---

## What Ana actually does today (operator reality)

| Step | Tool today | MVP automation target |
|------|------------|----------------------|
| 1. Pick theme from brand-pack | Cursor + content-plan | F5 content-plan helper |
| 2. Draft post text | `brand-grounded-copy` skill | F2 draft generation |
| 3. Check TBD / claims / CTA | Manual + skill | F3 brand check |
| 4. Pack for founder | `post-for-approval.md` | F4 + F6 export |
| 5. Pack for publish | `image-prompt-pack.md` + visuals | F6 export |
| 6. Log founder reply | `founder-inbox.md`, `decision-log.md` | Manual (Phase 2+ webhook) |
| 7. Publish | **Blocked** — no access | Out of scope |

---

## Cherry-pick from AiFinPay-smm (later, not fork)

| Asset | Use |
|-------|-----|
| `apps/api/tests/test_knowledge.py` | Ingest/search test patterns |
| `apps/api/tests/test_security.py` | Workspace isolation ideas (when multi-tenant) |
| HITL state flow docs | Approval status enum design |
| `fixtures/aifinpay-brand.md` | Cross-check against local brand-pack (do not publish client pack) |

---

## Decision log

| Question | Answer |
|----------|--------|
| Restart from scratch? | **No** — extend local skeleton + keep operator files |
| Fork AiFinPay-smm? | **No** — too much to delete; reference only |
| Is Phase 0 doc the MVP plan? | **No** — use `SOW.md` + `PLAN-MVP.md`; Phase 0 is north star for v2 |
| Is Google Sheet authoritative? | **No** — empty/wrong tab |

---

*Last updated: 2026-07-24*
