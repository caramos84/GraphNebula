from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.assets import router as assets_router
from app.core.config import PREVIEWS_DIR
from app.db.database import Base, engine
from app.models import asset, layout_feature, text_block, visual_region  # noqa: F401

Base.metadata.create_all(bind=engine)

app = FastAPI(title="DesignOps Visual Analysis MVP")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PREVIEWS_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/previews", StaticFiles(directory=PREVIEWS_DIR), name="previews")

app.include_router(assets_router, prefix="/api")


@app.get("/health")
def healthcheck():
    return {"status": "ok"}
