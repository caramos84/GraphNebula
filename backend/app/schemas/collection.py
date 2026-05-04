from datetime import datetime

from pydantic import BaseModel


class CollectionResponse(BaseModel):
    id: int
    brand_id: int
    name: str
    type: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
