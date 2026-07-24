# MVP Implementation Plan — Planning Only

> **Status:** Slice 1 done 2026-07-24 — brand ingest + eval green. Next: Slice 2 drafts.  
> **Canon for scope:** [`SOW.md`](../SOW.md) · **Tasks:** [`TODO-MVP.md`](./TODO-MVP.md) · **Gap:** [`GAP-ANALYSIS.md`](./GAP-ANALYSIS.md)

---

## 1. Problem statement

Ana spends significant time on repeatable work: drafting posts from brand-pack, checking claims/CTAs, and filling approval/designer templates. The org built a full SMM OS (`AiFinPay-smm`); the developer asked for a **smaller, operator-centric tool** planned before further coding. Ana's file-based workflow already works — the product should **accelerate** it, not replace it with a 28-agent platform.

---

## 2. Target architecture (trimmed)

### 2.1 Principles

1. **Operator-first** — markdown templates remain valid outputs until UI exists.
2. **Brand-pack is law** — no claim without citation; `TBD` blocks export.
3. **Human approval always** — no publish adapter in MVP.
4. **Single workspace** — AiFinPay only; auth deferred.
5. **Cursor-compatible** — CLI/API callable from existing skills.

### 2.2 Logical components

```mermaid
flowchart LR
    subgraph Local["Ana laptop (local-only)"]
        BP[knowledge/brand-pack-v1.md]
        SV[social-voice-v1.md]
        OP[operator/templates]
    end

    subgraph Product["smm OS apps/api"]
        ING[Ingest service]
        QD[(Qdrant)]
        DRAFT[Draft + QC service]
        EXP[Export service]
    end

    subgraph Human["Human gates"]
        ANA[Ana review]
        FOUNDER[Founder approve]
    end

    BP --> ING
    SV --> ING
    ING --> QD
    QD --> DRAFT
    DRAFT --> ANA
    ANA --> EXP
    EXP --> OP
    OP --> FOUNDER
```

### 2.3 Stack (MVP)

| Layer | Choice | Notes |
|-------|--------|-------|
| API | **FastAPI** (existing) | Keep `/health`, extend routers |
| Vector | **Qdrant Cloud** or local Docker | Already in skeleton |
| Embeddings | **Gemini** (config exists) or OpenAI | One provider only |
| LLM | **One** strong model via env | No LiteLLM router yet |
| Storage | **JSON/SQLite local** for drafts | No Supabase in MVP |
| UI | **None required** | Cursor + markdown; optional static page in slice 4 |
| Auth | **None** (local) | `demo_workspace_id` until v2 |
| Jobs | **Sync HTTP** | No Celery |

### 2.4 What we deliberately omit from Phase 0 docs

From `PHASE-0-PRODUCT.md`: Supabase RLS, LangGraph 5-node graph, Vercel dashboard, n8n Drive, Langfuse — **all deferred**. Reuse concepts (HITL, citations) without the infrastructure.

---

## 3. API surface (MVP target)

Base: `http://localhost:8000`

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/health` | Exists |
| POST | `/v1/ingest/text` | Exists — brand-pack chunks |
| POST | `/v1/search` | Exists — citation retrieval |
| POST | `/v1/drafts` | **New** — brief → draft + scorecard |
| GET | `/v1/drafts/{id}` | **New** — retrieve draft |
| POST | `/v1/drafts/{id}/export` | **New** — `{ format: "founder" \| "designer" \| "content-plan-row" }` |

No `/v1/runs`, no `/v1/approvals` DB until slice 3 justifies it.

---

## 4. First three build slices

### Slice 1 — Knowledge (≈2–3 days)

**Goal:** Brand-pack searchable with citations.

- Ingest script reading local `knowledge/*.md` (path via env, not committed).
- 10-question eval checklist in `eval/brand_questions.yaml`.
- README: how to run with `.env`.

**Done when:** 8/10 eval questions return correct brand-pack sections.

### Slice 2 — Draft + QC (≈2–3 days)

**Goal:** One-call grounded draft with flags.

- Prompt: platform + theme + retrieved chunks + social-voice rules.
- Post-process: regex/LLM check for `TBD`, non-`aifinpay.io` URLs, banned claims list from brand-pack.
- Return `{ draft, citations, scorecard, pass }`.

**Done when:** LI-1 regeneration matches quality of manual Wave 1 draft; flags catch intentional test violations.

### Slice 3 — Export (≈1–2 days)

**Goal:** Zero manual template filling.

- Map draft → `post-for-approval.md` sections.
- Map draft → `designer-brief.md` sections.
- Optional: emit content-plan row markdown for paste.

**Done when:** Ana runs one command and sends founder pack without editing structure.

---

## 5. Integration with Cursor / operator

| Today | After MVP |
|-------|-----------|
| `brand-grounded-copy` skill reads files | Skill calls `/v1/drafts` or CLI wrapper |
| Manual paste into templates | `/export` writes to `operator/outbox/` |
| `content-plan-14d.md` hand-edited | Helper emits row snippet |

**Do not remove skills** until API path is stable — parallel run during transition.

---

## 6. Risks & mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Founder expects full `AiFinPay-smm` on GitHub | Misaligned expectations | Send `SOW.md` summary tonight; show planning progress |
| Ana asked to docker-compose Postiz | Blocked, tired operator | Explicit out-of-scope; defer to dev |
| Two repos diverge | Confusion | Document: Ana repo = operator tool; org repo = reference/future merge |
| Brand-pack `TBD` lines | Bad drafts | Hard block on export if unresolved TBD in output |
| No GitHub org access for issues | Can't track in Jira/GitHub | Use local `TODO-MVP.md` until access fixed |
| Qdrant/LLM keys missing | Can't run slice 1 | `.env.example` + ask dev for shared dev keys |

---

## 7. Open questions for founder / dev

| # | Question | For |
|---|----------|-----|
| Q1 | Confirm **thin tool in Ana repo** vs continuing on `coinsecuritiescompany/AiFinPay-smm` | Dev (daochild / dev group) |
| Q2 | Can Ana get **read access** to org repo + GitHub issues? | Founder / platform |
| Q3 | Which **LLM key** should Ana use for local dev (DeepSeek/OpenAI)? | Dev |
| Q4 | Is **Qdrant Cloud** ok or local Docker only? | Dev |
| Q5 | Founder still **paused on content** until repo clear? | Founder |
| Q6 | Should planning docs be **committed/pushed** to Ana's remote now? | Founder (Ana waits for ask) |
| Q7 | Any **compliance** requirement to keep all generation on VPN/VPS? | Dev / compliance |

---

## 8. Success metrics (engineering)

| Metric | Target (MVP) |
|--------|--------------|
| Retrieval precision@5 | ≥70% on 10 brand questions |
| Draft generation latency | &lt;60s |
| False negative on TBD block | 0 on test set |
| Operator steps saved | ≥3 manual steps per post |

---

## 9. Relationship to full SMM OS vision

`docs/SMM-OS-PRODUCT-ARCHITECTURE.md` remains the **long-term north star** (multi-tenant SaaS). This MVP is a **strangler fig leaf**: each operator file replaced by automation per `operator/README.md` map. If the org later merges Ana's tool into `AiFinPay-smm`, slices 1–3 become modules (`knowledge_service`, `workflow`, `export`) — not a throwaway prototype.

---

## 10. Immediate next actions (after planning ack)

1. Dev/founder reply to Q1–Q3.
2. Start **TODO 1.1–1.5** (knowledge slice).
3. Ana continues **client-ops** on existing Wave 1 texts — no new posts until founder signals.

---

*Last updated: 2026-07-24 · Planning only — no code shipped*
