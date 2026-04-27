from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Asset(Base):
    __tablename__ = "assets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
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
