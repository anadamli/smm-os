# Шаг B — Аккаунты

Делай по порядку. После каждого пункта отметь `[x]` и сохрани секреты в одно место (1Password / заметка «SMM OS secrets» — **не** в GitHub и не в чат).

Время: ~30–45 минут, если аккаунты с нуля.

---

## B1. GitHub *(если ещё нет репо под продукт)*

1. Зайди на [github.com](https://github.com) → залогинься.
2. Пока **не обязательно** создавать репозиторий — я подготовлю каркас локально; репо создадим вместе.
3. Запомни свой GitHub username: `_______________`

- [ ] GitHub ок

---

## B2. Supabase *(коробка 3 — база фактов)*

1. Открой [supabase.com](https://supabase.com) → Start your project.
2. Create organization (любое имя, напр. `smm-os`).
3. **New project**:
   - Name: `smm-os-dev`
   - Database password: сгенерируй сильный → **сохрани**
   - Region: ближайший (Frankfurt `eu-central-1` ок для EU)
4. Дождись «Project is ready».
5. Settings → **API** → скопируй и сохрани:
   - Project URL
   - `anon` `public` key
   - `service_role` key (**секрет! не в фронт**)

- [ ] Проект создан
- [ ] URL + anon + service_role сохранены
- [ ] DB password сохранён

---

## B3. Qdrant Cloud *(коробка 4 — база знаний)*

1. Открой [cloud.qdrant.io](https://cloud.qdrant.io).
2. Создай cluster (Free tier достаточно).
3. Region: EU если есть.
4. Сохрани:
   - Cluster URL
   - API key

Пока **не** создавай collection руками — сделаем из кода / скриптом.

- [ ] Cluster есть
- [ ] URL + API key сохранены

---

## B4. LLM-ключи *(мозг будет звать модели)*

На P0 хватит **одного** сильного провайдера + потом добавим остальных.  
Рекомендация куратора: начни с **Anthropic** или **OpenAI** (что проще оплатить).

### Вариант A — OpenAI
1. [platform.openai.com](https://platform.openai.com) → API keys → Create.
2. Положи $5–10 баланса (иначе ключ мёртвый).

### Вариант B — Anthropic
1. [console.anthropic.com](https://console.anthropic.com) → API keys.

Позже: Gemini. Не блокирует старт.

- [ ] Хотя бы 1 LLM API key есть
- [ ] На ключе есть небольшой баланс

---

## B5. Пока НЕ обязательно (скажи, когда дойдём)

| Сервис | Зачем | Когда |
|---|---|---|
| Railway | Хостинг backend | Когда API уже запускается локально |
| Vercel | Панель | Когда будет web-приложение |
| Langfuse | Следить за агентами | Когда появится первый agent run |
| n8n | Google Drive | После «upload PDF → search» |
| Cloudflare | Домен/защита | Перед пилотом клиенту |

---

## Что прислать мне, когда готово

**Не присылай сами ключи в чат.**  
Напиши только:

```
B готово:
- Supabase: да/нет
- Qdrant: да/нет
- LLM: OpenAI / Anthropic / оба
- Регион Supabase: ...
```

Если что-то застряло (ошибка карты, не пускает регион) — опиши экран, разберём.

---

## Зачем эти три сервиса

```
Ты / панель
    ↓
Мозг (код)          ← пока на твоём компе, потом Railway
    ↓
Supabase  = кто ты, какие документы, черновики, approve
Qdrant    = «найди кусок текста про ICP»
LLM       = напиши / ответь
```

Без них продукт — только текст в Notion. С ними — уже настоящая система.
