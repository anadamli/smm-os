# MVP TODO — Sequential Build List

> Ordered tasks for **Ana's SMM Assistant** (thin tool). Each item ≈ 0.5–1 day solo.  
> **P0 alignment done 2026-07-24** — @pironmind: build thin tool in Ana repo; his AiFinPay-smm = production farm.

Legend: `[ ]` todo · `[~]` in progress · `[x]` done

---

## Phase 0 — Planning & alignment (no product code)

- [x] **P0.1** Write `SOW.md` with MVP scope and out-of-scope list *(2026-07-24)*
- [x] **P0.2** Write `docs/GAP-ANALYSIS.md` *(2026-07-24)*
- [x] **P0.3** Write `docs/PLAN-MVP.md` *(2026-07-24)*
- [x] **P0.4** Update `operator/founder-inbox.md` + day-status *(2026-07-24)* — note: `TOMORROW.md` pattern retired; use `operator/MAP.md` «Сейчас» only
- [x] **P0.5** Ana sent planning summary + repo question to @pironmind / group *(2026-07-24)*
- [x] **P0.6** Dev confirmed: thin tool in Ana repo; AiFinPay-smm = his farm / reference *(2026-07-24)*
- [x] **P0.7** Direction clear: two tracks (his prod farm vs Ana MVP); content still waits founder Wave 1 approve
- [ ] **P0.8** Create GitHub issues from Phase 1 tasks (optional — this TODO file is enough if issues blocked)

**P0 exit (2026-07-24):** Planning docs pushed to GitHub (`anadamli/smm-os`). Slice 1 unblocked.

---

## Phase 1 — Knowledge path (Slice 1)

- [x] **1.1** ADR: single workspace, no auth for local MVP; env-based workspace id *(docs/adr/001)*
- [x] **1.2** Script: ingest `knowledge/brand-pack-v1.md` + `social-voice-v1.md` *(scripts/ingest_brand_knowledge.py)*
- [x] **1.3** Verify search returns cited chunks for eval questions *(scripts/eval_brand_search.py)*
- [x] **1.4** Add `eval/brand_questions.yaml` — 10 retrieval Qs
- [x] **1.5** Document run steps in `apps/api/README.md`

**Exit:** Ana can ask "what is our ICP?" and get brand-pack-backed answer with citations.

---

## Phase 2 — Draft + brand check (Slice 2)

- [ ] **2.1** `POST /v1/drafts` — input: `{ platform, theme, brief }` → retrieval + LLM draft
- [ ] **2.2** Brand guardian pass: parse output for `TBD`, banned phrases, wrong URLs
- [ ] **2.3** Scorecard JSON: `{ citations[], flags[], pass: bool }`
- [ ] **2.4** Wire to Cursor skill or CLI: `python -m scripts.draft_post --platform linkedin --theme "..."` 
- [ ] **2.5** Human test: regenerate Wave 1 post (LI-1) and compare to manual draft in content-plan

**Exit:** Draft + QC in one command; flags visible before founder sees text.

---

## Phase 3 — Approval queue + export (Slice 3)

- [ ] **3.1** Persist drafts in SQLite or JSON under `operator/.drafts/` (local, gitignored)
- [ ] **3.2** Status flow: `draft → reviewed → ready_for_founder → approved | rejected`
- [ ] **3.3** Export markdown matching `operator/templates/post-for-approval.md`
- [ ] **3.4** Export designer brief matching `operator/templates/designer-brief.md`
- [ ] **3.5** Content-plan helper: append row to `content-plan-14d.md` format (or generate snippet for paste)

**Exit:** End-to-end brief → draft → QC → founder pack without manual template filling.

---

## Phase 4 — Hardening & visibility (optional week 2)

- [ ] **4.1** Minimal Next.js page: list pending approvals (read-only local)
- [ ] **4.2** GitHub Actions: lint + test on `apps/api` only
- [x] **4.3** README status table → link SOW + plan *(2026-07-27)*
- [ ] **4.4** Founder demo: 5-min screen recording of draft flow
- [ ] **4.5** Revisit: merge useful tests from `AiFinPay-smm` (isolation, ingest) — copy, don't fork

---

## Phase 5 — Explicitly deferred (do not start without new SOW)

- [ ] Supabase auth + multi-tenant RLS
- [ ] LangGraph multi-agent graph
- [ ] Google Drive / n8n webhooks
- [ ] Postiz / publish adapters
- [ ] Autopilot / Celery scheduler
- [ ] Analytics agent + weekly auto-report
- [ ] Telegram founder inbox webhook

---

## Dependency graph (summary)

```
P0 alignment → 1.x knowledge → 2.x draft+QC → 3.x export → 4.x polish
                     ↓
              (blocks everything)
```

---

*Last updated: 2026-07-27*
