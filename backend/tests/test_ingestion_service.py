import asyncio
from pathlib import Path

from PIL import Image

from app.models.visual_region import VisualRegion
from app.services.ingestion_service import IngestionService
from app.services.metadata_extractor import AssetMetadata
from app.services.region_detection_service import VisualRegionData


class FakeDB:
    def __init__(self):
        self.added = []
        self.commits = 0

    def add(self, obj):
        self.added.append(obj)

    def commit(self):
        self.commits += 1

    def refresh(self, _obj):
        return None


class FakeAsset:
    id = 123


class FakeUploadFile:
    def __init__(self, filename: str, content: bytes):
        self.filename = filename
        self._content = content

    async def read(self):
        return self._content


class FakeOCRService:
    def extract_text_blocks(self, _image):
        raise RuntimeError("tesseract not available")


class FakeRegionService:
    def detect_regions(self, _image):
        return [VisualRegionData(x=10, y=12, width=50, height=40, area=2000, relative_area=0.2)]


def test_ingestion_continues_when_ocr_unavailable(tmp_path):
    preview_path = Path(tmp_path) / "preview.jpg"
    Image.new("RGB", (100, 100), color="white").save(preview_path)

    ingestion = IngestionService()
    ingestion.ocr_service = FakeOCRService()
    ingestion.region_detection_service = FakeRegionService()

    fake_db = FakeDB()
    warnings = ingestion._extract_visual_structure(fake_db, FakeAsset(), preview_path)

    assert warnings
    assert "OCR skipped" in warnings[0]
    model_names = {obj.__class__.__name__ for obj in fake_db.added}
    assert "VisualRegion" in model_names
    assert "LayoutFeature" in model_names


def test_ingest_files_ocr_failure_returns_warning_not_error(tmp_path):
    preview_path = Path(tmp_path) / "preview.jpg"
    stored_path = Path(tmp_path) / "stored.png"
    Image.new("RGB", (100, 100), color="white").save(preview_path)

    ingestion = IngestionService()
    ingestion.ocr_service = FakeOCRService()
    ingestion.region_detection_service = FakeRegionService()

    metadata = AssetMetadata(
        original_filename="sample.png",
        extension=".png",
        mime_type="image/png",
        file_size=10,
        width=100,
        height=100,
        aspect_ratio="1.0000",
        is_animated=False,
        page_or_frame_count=1,
    )

    ingestion.metadata_extractor.extract = lambda _filename, _content: metadata
    ingestion.storage_service.save_upload = lambda _extension, _content: stored_path
    ingestion.storage_service.preview_path_for = lambda: preview_path
    ingestion.preview_generator.generate = lambda _ext, _content, _target: None

    fake_db = FakeDB()
    upload = FakeUploadFile("sample.png", b"fake")

    uploaded, errors, warnings = asyncio.run(ingestion.ingest_files(fake_db, [upload]))

    assert len(uploaded) == 1
    assert errors == []
    assert warnings and "OCR skipped" in warnings[0]["warning"]

    regions = [obj for obj in fake_db.added if isinstance(obj, VisualRegion)]
    assert len(regions) == 1
