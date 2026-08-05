"""SMM OS API — P0."""

from fastapi import FastAPI

from app.routers import drafts, knowledge

app = FastAPI(title="SMM OS API", version="0.2.0")
app.include_router(knowledge.router)
app.include_router(drafts.router)


@app.get("/health")
def health():
    return {"status": "ok", "service": "smm-os-api"}
