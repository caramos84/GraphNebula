from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
STORAGE_DIR = BASE_DIR / "storage"
UPLOADS_DIR = STORAGE_DIR / "uploads"
PREVIEWS_DIR = STORAGE_DIR / "previews"
DB_PATH = BASE_DIR / "assets.db"

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".pdf"}
SUPPORTED_MIME_TYPES = {
    "image/jpeg",
    "image/png",
    "image/gif",
    "application/pdf",
}
