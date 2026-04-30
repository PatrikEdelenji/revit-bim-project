import pandas as pd
from pathlib import Path


def load_rooms_parquet(path: str | Path) -> pd.DataFrame:
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"Parquet file not found: {path}")

    return pd.read_parquet(path)