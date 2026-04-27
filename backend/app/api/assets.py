from fastapi import APIRouter, Depends, File, Query, UploadFile
from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.asset import Asset
from app.schemas.asset import AssetResponse
from app.services.ingestion_service import IngestionService

router = APIRouter(prefix="/assets", tags=["assets"])
ingestion_service = IngestionService()


@router.post("/upload")
async def upload_assets(files: list[UploadFile] = File(...), db: Session = Depends(get_db)):
    assets, errors = await ingestion_service.ingest_files(db, files)
    return {
        "uploaded": [AssetResponse.model_validate(asset).model_dump() for asset in assets],
        "errors": errors,
    }


@router.get("", response_model=list[AssetResponse])
def list_assets(
    file_type: str | None = Query(default=None),
    min_width: int | None = Query(default=None),
    min_height: int | None = Query(default=None),
    aspect_ratio: str | None = Query(default=None),
    is_animated: bool | None = Query(default=None),
    db: Session = Depends(get_db),
):
    conditions = []

    if file_type:
        conditions.append(Asset.extension == file_type.lower())
    if min_width is not None:
        conditions.append(Asset.width >= min_width)
    if min_height is not None:
        conditions.append(Asset.height >= min_height)
    if aspect_ratio:
        conditions.append(Asset.aspect_ratio == aspect_ratio)
    if is_animated is not None:
        conditions.append(Asset.is_animated == is_animated)

    stmt = select(Asset).order_by(Asset.id.desc())
    if conditions:
        stmt = stmt.where(and_(*conditions))

    return list(db.scalars(stmt).all())
