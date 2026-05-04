from datetime import datetime

from pydantic import BaseModel


class BrandCreate(BaseModel):
    name: str
    description: str | None = None


class BrandResponse(BaseModel):
    id: int
    name: str
    description: str | None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
