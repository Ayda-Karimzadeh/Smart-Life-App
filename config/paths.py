from pathlib import Path
import sys

if getattr(sys, "frozen", False):
    APP_DIR = Path(sys.executable).parent
    RESOURCE_DIR = Path(sys._MEIPASS)
else:
    APP_DIR = Path(__file__).resolve().parent.parent
    RESOURCE_DIR = APP_DIR

DATA_DIR = APP_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

DB_PATH = DATA_DIR / "smart_life.db"
SCHEMA_PATH = RESOURCE_DIR / "database" / "schema.sql"