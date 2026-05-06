from pathlib import Path
import pandas as pd


def load_revit_rooms_json(file_path: str | Path) -> pd.DataFrame:
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    return pd.read_json(file_path)