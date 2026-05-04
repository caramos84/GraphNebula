from pathlib import Path
from uuid import uuid4

from app.core.config import PREVIEWS_DIR, UPLOADS_DIR


class StorageService:
    def save_upload(self, extension: str, content: bytes) -> Path:
        UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
        file_path = UPLOADS_DIR / f"{uuid4().hex}{extension}"
        file_path.write_bytes(content)
        return file_path

    def preview_path_for(self) -> Path:
        PREVIEWS_DIR.mkdir(parents=True, exist_ok=True)
        return PREVIEWS_DIR / f"{uuid4().hex}.jpg"
