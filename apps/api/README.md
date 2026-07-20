# SMM OS API

Minimal FastAPI app. Run later with:

```bash
cd apps/api
python -m venv .venv && source .venv/bin/activate
pip install fastapi uvicorn
uvicorn app.main:app --reload
```

Then open http://127.0.0.1:8000/health
