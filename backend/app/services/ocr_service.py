from __future__ import annotations

from dataclasses import dataclass

from PIL import Image

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
    def extract_text_blocks(self, image: Image.Image) -> list[OCRBlock]:
        if pytesseract is None:
            return []

        data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
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
