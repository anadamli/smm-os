"""SMM OS API — P0."""

from fastapi import FastAPI

from app.routers import knowledge

app = FastAPI(title="SMM OS API", version="0.1.0")
app.include_router(knowledge.router)


@app.get("/health")
def health():
    return {"status": "ok", "service": "smm-os-api"}
