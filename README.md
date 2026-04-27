# GraphNebula – DesignOps Visual Analysis MVP (Sprint 1)

This repository contains the first vertical MVP for an internal Design Operations visual analysis tool.

## Sprint 1 scope implemented

- Batch ingestion via drag-and-drop or file picker.
- Supported formats: JPG, PNG, GIF, PDF.
- Metadata extraction for each asset:
  - original filename
  - extension
  - MIME type
  - file size
  - dimensions
  - aspect ratio
  - static/animated status
  - page/frame count
- Thumbnail preview generation.
- SQLite asset catalog storage.
- Dashboard with card and table views.
- Filtering by file type, minimum dimensions, aspect ratio, and static/animated status.
- Error capture for unsupported/corrupt files.

## Architecture

```text
backend/
  app/
    api/               # FastAPI routers
    core/              # config constants
    db/                # SQLAlchemy DB setup
    models/            # ORM models
    schemas/           # Pydantic response schemas
    services/          # ingestion, metadata, preview, storage modules
  tests/               # metadata extraction tests
frontend/
  src/
    api/               # HTTP client + endpoints
    components/        # upload, filters, cards, table
    types/             # shared UI types
```

## Local setup

### 1) Backend (FastAPI)

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Backend health: <http://localhost:8000/health>

### 2) Frontend (React + Vite)

```bash
cd frontend
npm install
npm run dev
```

Frontend app: <http://localhost:5173>

## Run tests

```bash
cd backend
PYTHONPATH=. pytest
```

## Notes / out of scope in Sprint 1

Not implemented yet (intentionally): OCR, CV feature extraction, embeddings, clustering, heatmaps, LLM analysis.
