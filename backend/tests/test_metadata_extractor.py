import io

import fitz
import pytest
from PIL import Image

from app.services.metadata_extractor import CorruptedFileError, MetadataExtractor, UnsupportedFileError


def create_png(width=100, height=50):
    img = Image.new("RGB", (width, height), color="red")
    buff = io.BytesIO()
    img.save(buff, format="PNG")
    return buff.getvalue()


def create_gif_animated():
    img1 = Image.new("RGB", (64, 64), color="blue")
    img2 = Image.new("RGB", (64, 64), color="green")
    buff = io.BytesIO()
    img1.save(buff, format="GIF", save_all=True, append_images=[img2], loop=0, duration=100)
    return buff.getvalue()


def create_pdf():
    doc = fitz.open()
    doc.new_page(width=200, height=100)
    doc.new_page(width=400, height=200)
    data = doc.tobytes()
    doc.close()
    return data


def test_extract_png_metadata():
    extractor = MetadataExtractor()
    data = create_png()

    metadata = extractor.extract("artifact.png", data)

    assert metadata.extension == ".png"
    assert metadata.mime_type == "image/png"
    assert metadata.width == 100
    assert metadata.height == 50
    assert metadata.aspect_ratio == "2.0000"
    assert metadata.is_animated is False
    assert metadata.page_or_frame_count == 1


def test_extract_animated_gif_metadata():
    extractor = MetadataExtractor()
    data = create_gif_animated()

    metadata = extractor.extract("motion.gif", data)

    assert metadata.extension == ".gif"
    assert metadata.is_animated is True
    assert metadata.page_or_frame_count == 2


def test_extract_pdf_metadata():
    extractor = MetadataExtractor()
    data = create_pdf()

    metadata = extractor.extract("deck.pdf", data)

    assert metadata.extension == ".pdf"
    assert metadata.mime_type == "application/pdf"
    assert metadata.page_or_frame_count == 2
    assert metadata.width == 200
    assert metadata.height == 100


def test_unsupported_extension_raises():
    extractor = MetadataExtractor()

    with pytest.raises(UnsupportedFileError):
        extractor.extract("notes.txt", b"abc")


def test_corrupted_png_raises():
    extractor = MetadataExtractor()

    with pytest.raises(CorruptedFileError):
        extractor.extract("broken.png", b"not a real image")
