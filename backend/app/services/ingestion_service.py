from __future__ import annotations

from dataclasses import asdict
from datetime import datetime
from pathlib import Path

from fastapi import UploadFile
from PIL import Image
from sqlalchemy.orm import Session

from app.models.asset import Asset
from app.models.brand import Brand
from app.models.collection import Collection
from app.models.layout_feature import LayoutFeature
from app.models.text_block import TextBlock
from app.models.visual_region import VisualRegion
from app.services.layout_feature_service import LayoutFeatureService
from app.services.metadata_extractor import CorruptedFileError, MetadataExtractor, UnsupportedFileError
from app.services.ocr_service import OCRService
from app.services.preview_generator import PreviewGenerator
from app.services.region_detection_service import RegionDetectionService
from app.services.storage_service import StorageService


class IngestionService:
    def __init__(self) -> None:
        self.metadata_extractor = MetadataExtractor()
        self.preview_generator = PreviewGenerator()
        self.storage_service = StorageService()
        self.ocr_service = OCRService()
        self.region_detection_service = RegionDetectionService()
        self.layout_feature_service = LayoutFeatureService()

    async def ingest_files(
        self,
        db: Session,
        files: list[UploadFile],
        brand_id: int,
        collection_name: str | None = None,
    ) -> tuple[list[Asset], list[dict], list[dict], dict | None]:
        stored_assets: list[Asset] = []
        errors: list[dict] = []
        warnings: list[dict] = []

        brand = db.get(Brand, brand_id)
        if not brand:
            return [], [{"filename": "*", "error": f"Brand {brand_id} not found"}], [], None

        normalized_name = (collection_name or "").strip()
        if not normalized_name:
            normalized_name = f"{brand.name} — Upload {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}"
        collection = Collection(brand_id=brand.id, name=normalized_name, type="upload")
        db.add(collection)
        db.commit()
        db.refresh(collection)

        for file in files:
            content = await file.read()
            try:
                metadata = self.metadata_extractor.extract(file.filename, content)
                stored_path = self.storage_service.save_upload(metadata.extension, content)
                preview_file_path = self.storage_service.preview_path_for()
                self.preview_generator.generate(metadata.extension, content, preview_file_path)

                asset = Asset(
                    **asdict(metadata),
                    brand_id=brand.id,
                    collection_id=collection.id,
                    stored_path=str(stored_path),
                    preview_path=f"/previews/{preview_file_path.name}",
                )
                db.add(asset)
                db.commit()
                db.refresh(asset)

                extraction_warnings = self._extract_visual_structure(db, asset, preview_file_path)
                for warning in extraction_warnings:
                    warnings.append({"filename": file.filename, "warning": warning})

                db.refresh(asset)
                stored_assets.append(asset)
            except (UnsupportedFileError, CorruptedFileError, ValueError) as exc:
                errors.append({"filename": file.filename, "error": str(exc)})
            except Exception as exc:  # noqa: BLE001
                errors.append({"filename": file.filename, "error": f"Unexpected processing error: {exc}"})

        collection_payload = None
        if collection is not None:
            collection_payload = {
                "id": collection.id,
                "brand_id": collection.brand_id,
                "name": collection.name,
                "type": collection.type,
            }

        return stored_assets, errors, warnings, collection_payload

    def _extract_visual_structure(self, db: Session, asset: Asset, preview_file_path: Path) -> list[str]:
        warnings: list[str] = []

        with Image.open(preview_file_path) as preview_image:
            rgb_image = preview_image.convert("RGB")
            canvas_width, canvas_height = rgb_image.size

            text_blocks = []
            try:
                text_blocks = self.ocr_service.extract_text_blocks(rgb_image)
                if self.ocr_service.last_warning:
                    warnings.append(self.ocr_service.last_warning)
            except Exception as exc:  # noqa: BLE001
                warnings.append(f"OCR skipped due to unexpected failure: {exc}")

            regions = self.region_detection_service.detect_regions(rgb_image)

            text_features = self.layout_feature_service.compute_for_text_blocks(text_blocks, canvas_width, canvas_height)
            region_features = self.layout_feature_service.compute_for_regions(regions, canvas_width, canvas_height)

            for block in text_blocks:
                db.add(
                    TextBlock(
                        asset_id=asset.id,
                        text=block.text,
                        x=block.x,
                        y=block.y,
                        width=block.width,
                        height=block.height,
                        confidence=block.confidence,
                    )
                )

            for region in regions:
                db.add(
                    VisualRegion(
                        asset_id=asset.id,
                        x=region.x,
                        y=region.y,
                        width=region.width,
                        height=region.height,
                        area=region.area,
                        relative_area=region.relative_area,
                    )
                )

            for feature in [*text_features, *region_features]:
                db.add(
                    LayoutFeature(
                        asset_id=asset.id,
                        source_type=feature.source_type,
                        source_index=feature.source_index,
                        vertical_position=feature.vertical_position,
                        horizontal_position=feature.horizontal_position,
                        area_ratio=feature.area_ratio,
                        text_density=feature.text_density,
                    )
                )

            db.commit()

        return warnings
