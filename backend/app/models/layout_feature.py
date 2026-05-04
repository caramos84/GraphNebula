from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class LayoutFeature(Base):
    __tablename__ = "layout_features"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    asset_id: Mapped[int] = mapped_column(ForeignKey("assets.id", ondelete="CASCADE"), index=True)
    source_type: Mapped[str] = mapped_column(String, nullable=False)  # text_block or visual_region
    source_index: Mapped[int] = mapped_column(Integer, nullable=False)
    vertical_position: Mapped[str] = mapped_column(String, nullable=False)
    horizontal_position: Mapped[str] = mapped_column(String, nullable=False)
    area_ratio: Mapped[float] = mapped_column(Float, nullable=False)
    text_density: Mapped[float | None] = mapped_column(Float, nullable=True)
