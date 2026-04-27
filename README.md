# GraphNebula – DesignOps Visual Analysis MVP

This repository contains the first vertical MVP for an internal Design Operations visual analysis tool, now extended with Sprint 2 layout extraction.

## Implemented scope

### Sprint 1
- Batch ingestion via drag-and-drop or file picker.
- Supported formats: JPG, PNG, GIF, PDF.
- Metadata extraction (filename, MIME, extension, size, dimensions, aspect ratio, animated/static, frame/page count).
- Preview generation and SQLite asset catalog.
- Dashboard card and table views with filters.

### Sprint 2
- OCR extraction with `pytesseract`:
  - text
  - bounding box
  - confidence
- Basic visual region detection with OpenCV contours:
  - bounding box
  - area
  - relative area
- Structural feature extraction for text blocks and regions:
  - vertical position (`top/middle/bottom`)
  - horizontal position (`left/center/right`)
  - area ratio
  - text density (for OCR blocks)
- Persistence tables:
  - `text_blocks`
  - `visual_regions`
  - `layout_features`
- API responses now include OCR, detected regions, and layout features for each asset.
- OCR is optional at runtime: if the Tesseract binary is unavailable, upload still succeeds and region/layout extraction continues with OCR warnings.

## Architecture

```text
backend/
  app/
    api/
    core/
    db/
    models/
      asset.py
      text_block.py
      visual_region.py
      layout_feature.py
    schemas/
    services/
      ingestion_service.py
      metadata_extractor.py
      preview_generator.py
      storage_service.py
      ocr_service.py
      region_detection_service.py
      layout_feature_service.py
  tests/
frontend/
  src/
    api/
    components/
    types/
```

## Local setup

### Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Run tests
```bash
cd backend
PYTHONPATH=. pytest
```

## Not in scope yet
- Component classification (CTA/logo/etc.)
- Embeddings
- Clustering
- Advanced ML/CV models
