from pydantic import BaseModel, ConfigDict


class TextBlockResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    text: str
    x: int
    y: int
    width: int
    height: int
    confidence: float


class VisualRegionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    x: int
    y: int
    width: int
    height: int
    area: int
    relative_area: float


class LayoutFeatureResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    source_type: str
    source_index: int
    vertical_position: str
    horizontal_position: str
    area_ratio: float
    text_density: float | None


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
    brand_id: int | None = None
    collection_id: int | None = None


class AssetResponse(AssetBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    text_blocks: list[TextBlockResponse]
    visual_regions: list[VisualRegionResponse]
    layout_features: list[LayoutFeatureResponse]
