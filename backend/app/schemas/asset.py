from pydantic import BaseModel


class AssetBase(BaseModel):
    original_filename: str
    extension: str
    mime_type: str
    file_size: int
    width: int | None
    height: int | None
    aspect_ratio: str | None
    is_animated: bool
    page_or_frame_count: int | None
    preview_path: str | None


class AssetResponse(AssetBase):
    id: int

    class Config:
        from_attributes = True
