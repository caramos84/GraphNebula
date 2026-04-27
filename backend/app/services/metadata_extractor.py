from __future__ import annotations

import io
import mimetypes
from dataclasses import dataclass
from pathlib import Path

import fitz
from PIL import Image, UnidentifiedImageError

from app.core.config import SUPPORTED_EXTENSIONS, SUPPORTED_MIME_TYPES


class UnsupportedFileError(Exception):
    pass


class CorruptedFileError(Exception):
    pass


@dataclass
class AssetMetadata:
    original_filename: str
    extension: str
    mime_type: str
    file_size: int
    width: int | None
    height: int | None
    aspect_ratio: str | None
    is_animated: bool
    page_or_frame_count: int | None


class MetadataExtractor:
    def extract(self, filename: str, content: bytes) -> AssetMetadata:
        extension = Path(filename).suffix.lower()
        mime_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"

        if extension == ".jpeg":
            extension = ".jpg"
            mime_type = "image/jpeg"

        if extension not in SUPPORTED_EXTENSIONS or mime_type not in SUPPORTED_MIME_TYPES:
            raise UnsupportedFileError(f"Unsupported file type: {filename}")

        if extension == ".pdf":
            return self._extract_pdf(filename, extension, mime_type, content)

        return self._extract_image(filename, extension, mime_type, content)

    def _extract_pdf(self, filename: str, extension: str, mime_type: str, content: bytes) -> AssetMetadata:
        try:
            with fitz.open(stream=content, filetype="pdf") as doc:
                page_count = doc.page_count
                width, height = None, None
                if page_count > 0:
                    rect = doc.load_page(0).rect
                    width, height = int(rect.width), int(rect.height)
        except Exception as exc:  # noqa: BLE001
            raise CorruptedFileError(f"Could not read PDF: {filename}") from exc

        return AssetMetadata(
            original_filename=filename,
            extension=extension,
            mime_type=mime_type,
            file_size=len(content),
            width=width,
            height=height,
            aspect_ratio=self._aspect_ratio(width, height),
            is_animated=False,
            page_or_frame_count=page_count,
        )

    def _extract_image(self, filename: str, extension: str, mime_type: str, content: bytes) -> AssetMetadata:
        try:
            with Image.open(io.BytesIO(content)) as img:
                width, height = img.size
                frame_count = getattr(img, "n_frames", 1)
                is_animated = bool(getattr(img, "is_animated", False) or frame_count > 1)
        except UnidentifiedImageError as exc:
            raise CorruptedFileError(f"Could not parse image: {filename}") from exc
        except Exception as exc:  # noqa: BLE001
            raise CorruptedFileError(f"Unexpected image parsing error: {filename}") from exc

        return AssetMetadata(
            original_filename=filename,
            extension=extension,
            mime_type=mime_type,
            file_size=len(content),
            width=width,
            height=height,
            aspect_ratio=self._aspect_ratio(width, height),
            is_animated=is_animated,
            page_or_frame_count=frame_count if frame_count > 1 else 1,
        )

    @staticmethod
    def _aspect_ratio(width: int | None, height: int | None) -> str | None:
        if not width or not height:
            return None
        return f"{round(width / height, 4):.4f}"
