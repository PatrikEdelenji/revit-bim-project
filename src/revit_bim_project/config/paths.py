from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

RAW_ROOMS_PATH = RAW_DATA_DIR / "revit_rooms_export.txt"
PROCESSED_ROOMS_PATH = PROCESSED_DATA_DIR / "rooms.parquet"