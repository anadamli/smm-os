# SMM OS — Phase 0 Implementation Plan

> **Superseded.** Актуальный P0 продукта: [PHASE-0-PRODUCT.md](./PHASE-0-PRODUCT.md). Канон архитектуры: [SMM-OS-PRODUCT-ARCHITECTURE.md](./SMM-OS-PRODUCT-ARCHITECTURE.md).

**Статус (eng):** superseded  
**Длительность:** 8 недель (2 месяца)  
**Источник:** [SMM-OS-ARCHITECTURE.md](./SMM-OS-ARCHITECTURE.md) §12.2  
**Правило фазы:** не писать Production-агентов и publishing. Только фундамент + 2 sandbox-агента + eval.

---

## 1. Цель фазы

Построить **минимальный, но правильный** фундамент, на котором можно доказать:

1. Документы компании попадают в Knowledge Base.
2. Поиск по знаниям даёт релевантные ответы (>70% precision на eval-set).
3. Research Agent отвечает по продукту/бренду с цитатами источников.
4. Copywriter Agent пишет on-brand draft, который человек правит.
5. Всё наблюдаемо, с cost tracking и human-approve-all.

**Не цель Phase 0:** 30 агентов, Slack ingestion, автопубликация, multi-platform, learning loop.

---

## 2. Locked Tech Stack (Phase 0)

Минимальный стек. Не менять без ADR (Architecture Decision Record).

| Слой | Выбор Phase 0 | Почему | Отложить до |
|---|---|---|---|
| Runtime | Python 3.12 + FastAPI | Быстрый прототип агентов, MCP-экосистема | — |
| Orchestration | LangGraph (single process) | Достаточно для 2 агентов; Temporal — Phase 2 | Phase 2 → Temporal |
| LLM Gateway | LiteLLM | Multi-model, cost logs | — |
| Primary LLM | Claude Sonnet (or GPT-4.1-class) | Quality для Research/Copy | — |
| Cheap LLM | Claude Haiku / GPT-4o-mini | Summaries, chunking helpers | — |
| Embeddings | `text-embedding-3-large` (или аналог) | Quality first; cost OK на 10–50 docs | Phase 1 A/B |
| Document Store | PostgreSQL 16 | Single source of truth | — |
| Vector | pgvector (в том же Postgres) | Один DB, меньше ops | Phase 1 → Qdrant если нужно |
| Object Storage | Local FS → S3/GCS | Local OK в weeks 1–4 | Week 5+ cloud |
| Queue | Redis (optional) / in-process | Не нужен Kafka | Phase 3 |
| Secrets | `.env` + Doppler/1Password (dev) | Vault — Phase 1+ | Phase 1 |
| Observability | Structured JSON logs + simple cost table | OTel/Grafana — Phase 1 | Phase 1 |
| Ingestion | Google Drive API + Notion API | Core corpus | Phase 1 → PDF/Word/web |
| Tool protocol | MCP servers (Drive, Notion, Search) | Соответствует архитектуре | — |
| UI | CLI + простой web chat (опционально) | Не строить dashboard | Phase 1 admin UI |
| Hosting | Local Docker Compose → single VPS | <$50/mo | Phase 1 cloud |

### ADR-обязательные решения до Week 2

Зафиксировать в `docs/adr/`:

1. **ADR-001** — LangGraph vs Temporal (Phase 0 = LangGraph).
2. **ADR-002** — pgvector vs отдельный Qdrant.
3. **ADR-003** — Primary LLM vendor + fallback.
4. **ADR-004** — Chunking strategy v0 (size, overlap, separators).
5. **ADR-005** — Metadata schema v0.

---

## 3. Scope Freeze

### In scope

- Repo skeleton + Docker Compose (Postgres+pgvector, Redis optional, app)
- Document inventory (core 10–20 docs)
- Ingestion: Google Drive + Notion (markdown/docs)
- Chunking + embeddings + metadata
- Vector search API (`/search`)
- Eval dataset (30–50 Q/A pairs) + scoring script
- Agent contracts: Research, Copywriter (sandbox)
- Manual workflow: human prompt → agent → draft → human edit
- Cost tracking per request
- Basic auth for API (API key)
- Runbooks: ingest, search, agent invoke

### Explicitly out of scope

- Slack / Telegram / Discord ingestion
- Publishing to any social platform
- Graph DB (Neo4j)
- Hybrid search (BM25) — Phase 1
- Conflict detection automation — Phase 1
- Memory beyond session/working — Phase 2
- >2 agents
- Multi-tenant
- Auto-approve anything

---

## 4. Exit Criteria (Definition of Done)

Phase 0 **закрыта**, только если все пункты true:

| # | Criterion | How to verify |
|---|---|---|
| E1 | ≥10 core documents ingested, 100% of inventory list | Inventory checklist signed |
| E2 | Vector search precision@5 ≥70% on eval set | `scripts/eval_retrieval.py` report |
| E3 | Research Agent: 8/10 questions answered with correct source citations | Manual eval sheet |
| E4 | Copywriter: 5 drafts judged “usable with light edit” by human | Review log |
| E5 | End-to-end latency: question → answer <60s (p95) | Traces / logs |
| E6 | Cost dashboard: daily spend visible; budget alerts at $X | Cost table query |
| E7 | Monitoring: app/Postgres up; ingest failures alert | Healthcheck + alert test |
| E8 | ADRs 001–005 written and accepted | `docs/adr/` |
| E9 | No production publishing credentials in repo | Secret scan |

---

## 5. Team & Roles (даже если 1 человек)

| Role | Responsibility | Hours/week (ideal) |
|---|---|---|
| Architect / You | Scope freeze, ADRs, eval judgment, brand docs | 6–10 |
| Platform Engineer | Infra, DB, ingestion, API | 15–20 |
| AI Engineer | Chunking, retrieval, agents, eval scripts | 15–20 |
| Domain Owner (Founder/Marketing) | Core doc list, ToV examples, approve drafts | 3–5 |

Solo mode: compress to 8 weeks with reduced hours on polish; **не** расширять scope.

---

## 6. Week-by-Week Plan

### Week 1 — Inventory & Decisions

**Goal:** Знать, что ingest'ить, и зафиксировать стек.

| Task | Owner | Output |
|---|---|---|
| Audit all knowledge sources (Drive folders, Notion spaces) | Domain | Source map spreadsheet |
| Select **Core Corpus v0** (10–20 docs): brandbook, ToV, ICP, product, FAQ, positioning | Domain + Architect | `docs/corpus-inventory.md` |
| Create repo skeleton (`apps/`, `packages/`, `docs/adr/`, `scripts/`, `eval/`) | Eng | Repo structure |
| Write ADR-001…005 drafts | Architect | ADRs |
| Get Google + Notion API credentials (read-only) | Eng | Secrets in vault/env |
| Define eval questions draft (20+) | Domain | `eval/questions.draft.yaml` |

**Week 1 Done when:** inventory signed, credentials work, ADRs drafted.

---

### Week 2 — Infrastructure Skeleton

**Goal:** `docker compose up` → Postgres+pgvector+API health.

| Task | Owner | Output |
|---|---|---|
| Docker Compose: Postgres 16 + pgvector, app service | Eng | `compose.yaml` |
| Schema v0: `documents`, `chunks`, `embeddings`, `ingest_runs`, `cost_events` | Eng | SQL migrations |
| LiteLLM proxy configured (2 models) | Eng | Working `/v1/chat` |
| Health endpoints + structured logging | Eng | `/health`, JSON logs |
| Cost event writer (model, tokens, $) | Eng | Table + helper |
| Secret management pattern documented | Eng | `docs/runbooks/secrets.md` |

**Week 2 Done when:** empty KB API runs locally; cost events record a test call.

---

### Week 3 — Ingestion Pipeline v0

**Goal:** Drive + Notion → raw store → chunks → embeddings.

| Task | Owner | Output |
|---|---|---|
| Google Drive connector (list + download by folder IDs) | Eng | MCP or internal connector |
| Notion connector (pages/databases from allowlist) | Eng | Connector |
| Normalizer: PDF/DOCX→text later; Week 3 = Google Docs export + Notion MD | Eng | Text pipeline |
| Chunker v0 per ADR-004 | AI | Chunks with metadata |
| Embed + upsert to pgvector | AI | Searchable KB |
| Idempotent re-ingest (content hash) | Eng | No duplicates |
| Ingest CLI: `ingest run --source drive\|notion` | Eng | Runbook |

**Metadata v0 (обязательные поля):**

```yaml
document_id: uuid
source: drive|notion
source_uri: string
title: string
doc_type: brand|product|strategy|icp|faq|other
authority: 1-5          # brandbook=5, draft notes=2
language: ru|en|...
version: string|null
updated_at_source: datetime
ingested_at: datetime
partition: core|brand|product|strategy
tags: [string]
pii_flag: false
```

**Week 3 Done when:** all Core Corpus docs searchable via SQL/API.

---

### Week 4 — Retrieval + Eval Framework

**Goal:** Измеримое качество поиска до агентов.

| Task | Owner | Output |
|---|---|---|
| Search API: semantic top-k + metadata filters | AI | `POST /search` |
| Citation format: chunk_id, title, uri, score | AI | Response schema |
| Finalize eval set: 30–50 questions with expected docs/chunks | Domain + AI | `eval/retrieval.yaml` |
| Eval runner: precision@5, recall@5, MRR | AI | `scripts/eval_retrieval.py` |
| Baseline report + failure analysis | AI | `eval/reports/week4.md` |
| Tune: chunk size / overlap / top-k (max 3 experiments) | AI | Chosen config in ADR-004 update |

**Week 4 Done when:** precision@5 ≥70% **или** documented gap plan with owner (max 1 week slip).

---

### Week 5 — Research Agent (Sandbox)

**Goal:** Первый специалист, который отвечает только из KB (+ optional web later off).

| Task | Owner | Output |
|---|---|---|
| Agent contract YAML (inputs/outputs/tools/limits) | Architect | `agents/research.contract.yaml` |
| LangGraph: retrieve → synthesize → cite → refuse if weak evidence | AI | Research Agent |
| Tools: `kb.search`, `kb.get_document` only (no web yet) | AI | Tool bindings |
| Refusal policy: if score < threshold → ask clarifying / escalate | AI | Prompt + tests |
| Human UI: CLI `ask "Что такое наш ICP?"` | Eng | CLI |
| Manual eval: 10 questions scored | Domain | Score sheet ≥8/10 |

**Limitations (hard):**
- No publishing
- No memory write to long-term
- No web search in Phase 0 (optional flag OFF)
- Max 8 retrieval calls / request

**Week 5 Done when:** E3 met.

---

### Week 6 — Copywriter Agent (Sandbox)

**Goal:** Draft posts/captions с ToV, grounded in brand docs.

| Task | Owner | Output |
|---|---|---|
| Agent contract | Architect | `agents/copywriter.contract.yaml` |
| Inputs: brief, platform, length, CTA, forbidden claims | AI | Schema |
| Always retrieve Brand + ToV + product facts before writing | AI | Graph node |
| Output: draft + citations + confidence + “needs human” flags | AI | Structured output |
| Human review checklist (brand, facts, tone) | Domain | `docs/qc-checklist-v0.md` |
| 5 drafts produced and reviewed | Domain | Review log |

**Week 6 Done when:** E4 met.

---

### Week 7 — Glue Workflow + Hardening

**Goal:** Один human-triggered pipeline Research → Copywriter → human.

| Task | Owner | Output |
|---|---|---|
| Workflow: brief → Research pack → Copy draft → human approve | AI | `workflows/manual_content_v0` |
| Session logging (request_id, agents, costs, outputs) | Eng | Trace store |
| Rate limits + max $ per day | Eng | Config |
| Failure modes: empty KB, API down, low confidence | Eng | Runbook |
| Re-ingest schedule (manual or nightly cron) | Eng | Cron/docs |
| Security pass: secrets, PII in logs, redact | Eng | Checklist |

**Week 7 Done when:** E5–E7 met; one full demo for founder.

---

### Week 8 — Stabilize, Document, Gate Review

**Goal:** Закрыть Phase 0 gate.

| Task | Owner | Output |
|---|---|---|
| Fix remaining eval gaps | AI | Final eval report ≥70% |
| Update architecture doc with “as-built” notes (Phase 0) | Architect | Short delta section |
| Phase 0 retrospective (what broke, what to change) | All | `docs/retros/phase-0.md` |
| Phase 1 kickoff brief (hybrid search, Brand Agent, QC) | Architect | `docs/PHASE-1-KICKOFF.md` stub |
| Go / No-Go meeting | All | Signed DoD |

**Week 8 Done when:** all Exit Criteria E1–E9 checked.

---

## 7. Concrete Task Backlog (checkable)

### Foundations
- [ ] Repo + Compose + migrations
- [ ] LiteLLM + cost_events
- [ ] ADRs 001–005 accepted
- [ ] Corpus inventory (10–20) signed
- [ ] Google Drive read access
- [ ] Notion read access

### Knowledge
- [ ] Ingest Drive core docs
- [ ] Ingest Notion core pages
- [ ] Metadata schema enforced
- [ ] Content-hash idempotency
- [ ] Search API + citations
- [ ] Eval set 30–50
- [ ] precision@5 ≥70%

### Agents
- [ ] Research Agent contract + impl
- [ ] Copywriter Agent contract + impl
- [ ] Manual Research→Copy workflow
- [ ] Human QC checklist v0
- [ ] Research eval ≥8/10
- [ ] Copywriter 5 usable drafts

### Ops
- [ ] Healthchecks
- [ ] Cost daily report
- [ ] Budget alert
- [ ] Runbooks: ingest, ask, review
- [ ] Secret scan clean
- [ ] Phase 0 retro + Phase 1 stub

---

## 8. Eval Framework (обязателен с Week 1)

### 8.1 Retrieval Eval

```yaml
# eval/retrieval.yaml (example shape)
- id: Q001
  question: "Кто наш ICP для LinkedIn?"
  must_retrieve_doc_ids: [doc_icp_v2]
  nice_to_have: [doc_positioning]
  language: ru
```

Метрики: Precision@5, Recall@5, MRR. Gate: Precision@5 ≥ 0.70.

### 8.2 Agent Eval

| Agent | N cases | Pass rule |
|---|---|---|
| Research | 10 | Correct + cited; no hallucinated facts |
| Copywriter | 5 | Usable with ≤15 min human edit; on-brand |

### 8.3 Regression

Каждый merge, меняющий chunking/embeddings/prompts → прогон eval. Не деплоить, если precision упал >5 п.п.

---

## 9. Budget Guardrails

| Item | Phase 0 target |
|---|---|
| Infra (VPS/Docker) | ≤ $40/mo |
| LLM + embeddings | ≤ $150/mo (dev) |
| Soft alert | 80% of monthly LLM budget |
| Hard stop | 100% — agents refuse new requests |

Track per: `request_id`, `agent`, `model`, `input_tokens`, `output_tokens`, `usd`.

---

## 10. Human Workflow (как работать каждый день)

```
1. Domain Owner пишет brief (тема, платформа, цель)
2. Human запускает: research "..."
3. Читает Research pack + citations → correct/incorrect
4. Запускает: copywrite --from research_id
5. Правит draft по QC checklist
6. Логирует: что агент сделал хорошо / плохо (для Phase 5 learning)
7. Публикует человек вручную (вне системы)
```

Никакой auto-publish в Phase 0.

---

## 11. Risks & Mitigations (операционные)

| Risk | Signal | Mitigation |
|---|---|---|
| Scope creep (“добавим ещё TikTok agent”) | New agent PRs | Reject; park in Phase 2 backlog |
| Bad corpus (outdated positioning) | Conflicting answers | Authority + `updated_at`; Domain owns truth |
| Embedding/chunk fail | Low precision | Cap experiments to 3 configs in Week 4 |
| API access blocked | Empty ingest | Week 1 audit; escalate early |
| Cost spike | Daily $ jump | Hard stop + cheaper model for summarization |
| Solo burnout | Missed weeks | Cut polish, keep E1–E4 |

---

## 12. Deliverables Checklist (артефакты)

| Artifact | Path |
|---|---|
| Architecture (parent) | `docs/SMM-OS-ARCHITECTURE.md` |
| This plan | `docs/PHASE-0-IMPLEMENTATION.md` |
| ADRs | `docs/adr/001-*.md` … |
| Corpus inventory | `docs/corpus-inventory.md` |
| Agent contracts | `agents/*.contract.yaml` |
| Eval set | `eval/retrieval.yaml` |
| Eval reports | `eval/reports/` |
| Runbooks | `docs/runbooks/` |
| Retro | `docs/retros/phase-0.md` |
| Phase 1 stub | `docs/PHASE-1-KICKOFF.md` |

---

## 13. Handoff to Phase 1

Когда Phase 0 закрыта, Phase 1 стартует с:

1. Hybrid search (BM25 + dense)
2. Full source sync (<24h freshness)
3. Brand Agent + basic QC Agent
4. Knowledge partitions + admin view
5. Entity graph v0 (simple)
6. Conflict detection (manual resolve queue)

Не начинать Phase 1, пока E1–E4 не зелёные.

---

## 14. Immediate Next Actions (эта неделя)

Сделать **до** написания кода агентов:

1. **Составить Core Corpus v0** — список 10–20 документов с ссылками (Drive/Notion).
2. **Получить read-only credentials** Google Drive + Notion.
3. **Написать ADR-001…005** (даже коротко, ½ страницы каждый).
4. **Набросать 20 eval-вопросов** про бренд/продукт/ICP.
5. **Поднять Docker Compose** с Postgres+pgvector.

После этого — Week 3 ingestion.

---

**Owner:** Platform Architecture  
**Review cadence:** Weekly gate (пятница) — go/adjust/stop  
**Related:** Architecture §12.2, §5.5, §8 Knowledge System
