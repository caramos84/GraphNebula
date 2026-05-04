from __future__ import annotations

import logging
from dataclasses import dataclass

from PIL import Image

logger = logging.getLogger(__name__)

try:
    import pytesseract
except ImportError:  # pragma: no cover
    pytesseract = None


@dataclass
class OCRBlock:
    text: str
    x: int
    y: int
    width: int
    height: int
    confidence: float


class OCRService:
    def __init__(self) -> None:
        self.last_warning: str | None = None

    def extract_text_blocks(self, image: Image.Image) -> list[OCRBlock]:
        self.last_warning = None

        if pytesseract is None:
            self.last_warning = "pytesseract is not installed; OCR skipped."
            logger.warning(self.last_warning)
            return []

        tesseract_not_found_error = getattr(getattr(pytesseract, "pytesseract", None), "TesseractNotFoundError", None)
        tesseract_error = getattr(pytesseract, "TesseractError", None)

        handled_exceptions: tuple[type[BaseException], ...] = tuple(
            exc
            for exc in [tesseract_not_found_error, tesseract_error, RuntimeError, OSError]
            if isinstance(exc, type)
        )

        try:
            data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
        except handled_exceptions as exc:  # type: ignore[misc]
            self.last_warning = f"OCR skipped due to runtime error: {exc.__class__.__name__}: {exc}"
            logger.warning(self.last_warning)
            return []

        blocks: list[OCRBlock] = []
        n = len(data.get("text", []))

        for i in range(n):
            text = (data["text"][i] or "").strip()
            if not text:
                continue

            conf_raw = data["conf"][i]
            try:
                confidence = float(conf_raw)
            except (TypeError, ValueError):
                confidence = -1.0

            if confidence < 0:
                continue

            blocks.append(
                OCRBlock(
                    text=text,
                    x=int(data["left"][i]),
                    y=int(data["top"][i]),
                    width=int(data["width"][i]),
                    height=int(data["height"][i]),
                    confidence=confidence,
                )
            )

        return blocks
