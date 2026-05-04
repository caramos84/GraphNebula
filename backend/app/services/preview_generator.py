from __future__ import annotations

import io
from pathlib import Path

import fitz
from PIL import Image


class PreviewGenerator:
    def generate(self, extension: str, content: bytes, target_path: Path) -> None:
        target_path.parent.mkdir(parents=True, exist_ok=True)
        if extension == ".pdf":
            self._generate_pdf_preview(content, target_path)
        else:
            self._generate_image_preview(content, target_path)

    def _generate_image_preview(self, content: bytes, target_path: Path) -> None:
        with Image.open(io.BytesIO(content)) as img:
            if getattr(img, "is_animated", False):
                img.seek(0)
            thumbnail = img.convert("RGB")
            thumbnail.thumbnail((360, 360))
            thumbnail.save(target_path, format="JPEG", quality=80)

    def _generate_pdf_preview(self, content: bytes, target_path: Path) -> None:
        with fitz.open(stream=content, filetype="pdf") as doc:
            if doc.page_count == 0:
                raise ValueError("Cannot preview empty PDF")
            page = doc.load_page(0)
            pix = page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5), alpha=False)
            pix.save(target_path)
