from pathlib import Path
import os
import sys


def _get_writable_app_dir() -> Path:
    """Return a per-user writable directory for runtime data."""
    if sys.platform == "win32":
        appdata = os.environ.get("APPDATA")
        if appdata:
            return Path(appdata) / "Smart-Life-App"
        return Path.home() / "AppData" / "Roaming" / "Smart-Life-App"
    if sys.platform == "darwin":
        return Path.home() / "Library" / "Application Support" / "Smart-Life-App"
    return Path.home() / ".smart_life_app"


if getattr(sys, "frozen", False):
    RESOURCE_DIR = Path(sys._MEIPASS)
    APP_DIR = _get_writable_app_dir()
else:
    APP_DIR = Path(__file__).resolve().parent.parent
    RESOURCE_DIR = APP_DIR

APP_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR = APP_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = DATA_DIR / "smart_life.db"
SCHEMA_PATH = RESOURCE_DIR / "database" / "schema.sql"