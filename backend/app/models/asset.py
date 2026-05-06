from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Asset(Base):
    __tablename__ = "assets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    brand_id: Mapped[int | None] = mapped_column(ForeignKey("brands.id"), nullable=True, index=True)
    collection_id: Mapped[int | None] = mapped_column(ForeignKey("collections.id"), nullable=True, index=True)
    original_filename: Mapped[str] = mapped_column(String, nullable=False)
    extension: Mapped[str] = mapped_column(String, nullable=False, index=True)
    mime_type: Mapped[str] = mapped_column(String, nullable=False, index=True)
    file_size: Mapped[int] = mapped_column(Integer, nullable=False)
    width: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True)
    height: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True)
    aspect_ratio: Mapped[str | None] = mapped_column(String, nullable=True, index=True)
    is_animated: Mapped[bool] = mapped_column(Boolean, nullable=False, index=True)
    page_or_frame_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    stored_path: Mapped[str] = mapped_column(String, nullable=False)
    preview_path: Mapped[str | None] = mapped_column(String, nullable=True)

    brand = relationship("Brand", back_populates="assets")
    collection = relationship("Collection", back_populates="assets")
    text_blocks = relationship("TextBlock", cascade="all, delete-orphan", lazy="selectin")
    visual_regions = relationship("VisualRegion", cascade="all, delete-orphan", lazy="selectin")
    layout_features = relationship("LayoutFeature", cascade="all, delete-orphan", lazy="selectin")
    radar_metric = relationship("RadarMetric", cascade="all, delete-orphan", lazy="selectin", uselist=False)
