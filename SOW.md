# Statement of Work — Ana's SMM Assistant (MVP)

## Для Ани (кратко)

**Цель:** не «операционная система на 28 агентов», а **личный инструмент**, который экономит твоё время на текстах, проверке бренда и пакетах на согласование.

**Что строим:** тонкий слой поверх твоих файлов в `operator/` + `knowledge/brand-pack-v1.md` — с API/скриптом, который Cursor или простая форма может вызывать.

**Что НЕ строим:** автопостинг, 21 канал, аналитику, Postiz, multi-tenant SaaS, полный форк `AiFinPay-smm`.

**Решение:** §6 Option A **подтверждена @pironmind 24.07** — thin tool в твоём репо; `AiFinPay-smm` = его ферма / reference.

---

## 1. Background

AiFinPay needs consistent, brand-safe social content. Ana (operator) already runs a **file-based MVP** in `operator/` and `knowledge/` — content plans, approval packs, designer briefs, founder inbox. The org repo [`coinsecuritiescompany/AiFinPay-smm`](https://github.com/coinsecuritiescompany/AiFinPay-smm) is a **production-oriented beta** with FastAPI, Next.js, 28 agent roles, 21 channel contracts, Celery autopilot, Postiz, and analytics — designed for several isolated workspaces, not for Ana's immediate weekly workflow.

Developer guidance (@pironmind / gist by daochild, to Ana): **planning first**, then build; **reasonable features only**; tool that **saves operator time**; work in Ana's repo. **Confirmed 2026-07-24:** @pironmind finishes `AiFinPay-smm` as production “farm”; Ana builds a separate thin MVP — compare effectiveness later. The linked Google Sheet on "minimal functionality" was **wrong** (empty smart-contracts tab) — scope is derived from local operator reality + `brand-pack-v1.md` + Phase 0 docs, trimmed to Ana MVP.

---

## 2. Goal

Deliver a **personal, single-workspace SMM assistant** for AiFinPay content operations:

> **Ingest brand canon → generate grounded drafts → block bad claims → queue for human approval → export handoff packs.**

Success = Ana spends less time on repetitive copy/QC/packaging; founder still approves everything before publish.

---

## 3. In Scope (MVP — reasonable features)

| # | Feature | What it does for Ana |
|---|---------|----------------------|
| F1 | **Brand knowledge ingest** | Index `brand-pack-v1.md`, `social-voice-v1.md`, and approved source snippets into searchable store (start: markdown upload; no Drive OAuth in MVP). |
| F2 | **Grounded draft generation** | Input: platform + theme/brief → output: post text with citations to brand-pack sections. |
| F3 | **Brand / claim check** | Flag `TBD`, forbidden claims, off-brand tone, wrong CTA domain (must be `aifinpay.io` per founder decision). Block or warn before export. |
| F4 | **Human approval queue** | Drafts land in structured approval records (DB or markdown export matching `post-for-approval.md`). No publish side effect. |
| F5 | **Content plan helper** | Suggest or fill rows in 14-day plan format (`LI-1`, platform, theme, status). |
| F6 | **Export / handoff** | Generate designer brief + founder approve pack from approved draft (templates in `operator/templates/`). |

**Optional stretch (after F1–F6 stable):** single-page local UI or Cursor skill hook — not required for week-1 value.

---

## 4. Explicitly Out of Scope

| Area | Why out |
|------|---------|
| 28 agents / 18-stage orchestrator | Overkill; 3–4 logical steps (research → copy → brand check → HITL) suffice |
| 21 channel contracts + Postiz publish | Ana has no publish access; founder said planning first |
| Autopilot / Celery scheduled cycles | Operator-driven cadence; no autonomous posting |
| Multi-tenant SaaS, billing, self-serve signup | Single operator + founder approve |
| Full analytics / learning loop | Manual weekly metrics file stays |
| Web live research (Tavily/Serper) | Brand-pack is canon; web = Phase 2+ |
| Google Drive / Notion ingest | Manual markdown/PDF upload first |
| Docker Compose full stack tonight | Planning only until SOW approved |
| Visual/image generation | Designer owns visuals |
| Replacing Cursor skills entirely | Tool augments existing `brand-grounded-copy` workflow |

---

## 5. Success Criteria (Ana should feel within ~1 week)

| # | Criterion | How Ana knows it works |
|---|-----------|------------------------|
| S1 | **Faster drafts** | New post brief → grounded draft in one step (target: &lt;10 min vs ~30+ manual). |
| S2 | **Safer copy** | System surfaces `TBD`/forbidden claims before she sends to founder. |
| S3 | **Less copy-paste** | Approval pack + designer brief export matches existing templates. |
| S4 | **Same gates** | Nothing marked "published"; founder ✅ still required. |
| S5 | **Visible progress** | Planning docs + thin API in her GitHub repo; founder sees direction without operator files. |

---

## 6. Build Path Decision

| Option | Summary | Effort | Fit for Ana MVP |
|--------|---------|--------|-----------------|
| **A. Thin tool on current operator files** | Extend local `apps/api` skeleton; ingest brand-pack; CLI/Cursor-triggered draft + QC + markdown export | **Low–medium** | **✅ Recommended** |
| **B. Fork / slim `AiFinPay-smm`** | Strip 28 agents, Postiz, Celery, analytics from org repo | **High** (delete &gt;80% + re-learn stack) | ❌ Poor ROI |
| **C. Greenfield new repo** | Start empty | **Medium** | ❌ Duplicates existing local skeleton |

### Recommendation: **Option A — thin tool in Ana's repo (`smm OS`)**

**Rationale:**

1. Ana's **operator layer already works** — strangler map in `operator/README.md` maps files → future features.
2. Local repo has **Phase 0 canon docs** + minimal FastAPI (`/health`, `/v1/ingest/text`, `/v1/search`) — right foundation, wrong scope in `PHASE-0-PRODUCT.md` (trim tenancy/auth for MVP).
3. `AiFinPay-smm` is **~119 files**, demo-complete but requires Docker, Postiz keys, and ops Ana doesn't need this week.
4. Developer intent: **time-saving tool**, not OS — Option A delivers F1–F6 fastest without throwing away operator investment.

**Relationship to org repo:** Treat `AiFinPay-smm` as **reference implementation** (patterns for HITL, ingest tests) — not the codebase to fork. Reconcile with founder/dev after MVP slice 1.

---

## 7. Stakeholders & Approvals

| Role | Name | Decision needed |
|------|------|-----------------|
| Operator | Ana | Accept MVP scope; run file workflow during build |
| Developer | daochild / dev group | Confirm Option A vs org repo direction |
| Founder | AiFinPay | GitHub visibility; approve content (unchanged gate) |
| CMO/brand | — | Brand-pack remains canon |

---

## 8. Deliverables from Planning Phase (this week)

- [x] `SOW.md` (this file)
- [x] `docs/TODO-MVP.md` — sequential build tasks
- [x] `docs/GAP-ANALYSIS.md` — three-way comparison
- [x] `docs/PLAN-MVP.md` — architecture + first slices
- [ ] Founder/dev sign-off on Option A
- [ ] Slice 1 implementation (after sign-off)

---

## 9. References

- Local operator: `operator/README.md`, `operator/templates/`
- Brand canon: `knowledge/brand-pack-v1.md` (local only)
- Product north star (trimmed for MVP): `docs/SMM-OS-PRODUCT-ARCHITECTURE.md`, `docs/PHASE-0-PRODUCT.md`
- Org reference: `/Users/ana/Projects/work/AiFinPay-smm` (cloned locally)
- Dev onboarding gist: https://gist.github.com/daochild/98327b7f32e98c2e48086100b4335071

---

*Version: 2026-07-24 · Owner: Ana · Status: Planning — pending dev/founder ack*
