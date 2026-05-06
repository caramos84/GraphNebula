from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.brand import Brand
from app.models.collection import Collection
from app.schemas.brand import BrandCreate, BrandResponse
from app.schemas.collection import CollectionResponse

router = APIRouter(prefix="/brands", tags=["brands"])


@router.post("", response_model=BrandResponse)
def create_brand(payload: BrandCreate, db: Session = Depends(get_db)):
    existing = db.scalar(select(Brand).where(Brand.name == payload.name))
    if existing:
        raise HTTPException(status_code=400, detail="Brand name already exists")

    brand = Brand(name=payload.name, description=payload.description)
    db.add(brand)
    db.commit()
    db.refresh(brand)
    return brand


@router.get("", response_model=list[BrandResponse])
def list_brands(db: Session = Depends(get_db)):
    return list(db.scalars(select(Brand).order_by(Brand.name.asc())).all())


@router.get("/{brand_id}/collections", response_model=list[CollectionResponse])
def list_brand_collections(brand_id: int, db: Session = Depends(get_db)):
    brand = db.get(Brand, brand_id)
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")

    return list(db.scalars(select(Collection).where(Collection.brand_id == brand_id).order_by(Collection.id.desc())).all())
