from __future__ import annotations

from dataclasses import asdict

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.models.asset import Asset
from app.services.metadata_extractor import CorruptedFileError, MetadataExtractor, UnsupportedFileError
from app.services.preview_generator import PreviewGenerator
from app.services.storage_service import StorageService


class IngestionService:
    def __init__(self) -> None:
        self.metadata_extractor = MetadataExtractor()
        self.preview_generator = PreviewGenerator()
        self.storage_service = StorageService()

    async def ingest_files(self, db: Session, files: list[UploadFile]) -> tuple[list[Asset], list[dict]]:
        stored_assets: list[Asset] = []
        errors: list[dict] = []

        for file in files:
            content = await file.read()
            try:
                metadata = self.metadata_extractor.extract(file.filename, content)
                stored_path = self.storage_service.save_upload(metadata.extension, content)
                preview_file_path = self.storage_service.preview_path_for()
                self.preview_generator.generate(metadata.extension, content, preview_file_path)

                asset = Asset(
                    **asdict(metadata),
                    stored_path=str(stored_path),
                    preview_path=f"/previews/{preview_file_path.name}",
                )
                db.add(asset)
                db.commit()
                db.refresh(asset)
                stored_assets.append(asset)
            except (UnsupportedFileError, CorruptedFileError, ValueError) as exc:
                errors.append({"filename": file.filename, "error": str(exc)})
            except Exception as exc:  # noqa: BLE001
                errors.append({"filename": file.filename, "error": f"Unexpected processing error: {exc}"})

        return stored_assets, errors
