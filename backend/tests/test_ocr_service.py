from PIL import Image

import app.services.ocr_service as ocr_module
from app.services.ocr_service import OCRService


class FakeTesseractNotFoundError(Exception):
    pass


class FakeTesseractError(Exception):
    pass


class FakePytesseract:
    class Output:
        DICT = "dict"

    class pytesseract:
        TesseractNotFoundError = FakeTesseractNotFoundError

    TesseractError = FakeTesseractError

    @staticmethod
    def image_to_data(_image, output_type):
        assert output_type == "dict"
        return {
            "text": ["", "Hello", "World"],
            "left": [0, 10, 60],
            "top": [0, 15, 20],
            "width": [0, 45, 50],
            "height": [0, 20, 18],
            "conf": ["-1", "90", "80"],
        }


class FakePytesseractMissingBinary(FakePytesseract):
    @staticmethod
    def image_to_data(_image, output_type):
        raise FakeTesseractNotFoundError("tesseract binary not found")


def test_ocr_extracts_text_blocks(monkeypatch):
    monkeypatch.setattr(ocr_module, "pytesseract", FakePytesseract)
    service = OCRService()
    image = Image.new("RGB", (200, 100), color="white")

    blocks = service.extract_text_blocks(image)

    assert service.last_warning is None
    assert len(blocks) == 2
    assert blocks[0].text == "Hello"
    assert blocks[0].x == 10
    assert blocks[0].confidence == 90.0
    assert blocks[1].text == "World"


def test_ocr_missing_tesseract_binary_returns_empty(monkeypatch):
    monkeypatch.setattr(ocr_module, "pytesseract", FakePytesseractMissingBinary)
    service = OCRService()
    image = Image.new("RGB", (100, 80), color="white")

    blocks = service.extract_text_blocks(image)

    assert blocks == []
    assert service.last_warning is not None
    assert "OCR skipped" in service.last_warning
