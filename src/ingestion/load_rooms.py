from pathlib import Path
import pandas as pd


def load_rooms_csv(file_path: str | Path, skiprows: int = 0) -> pd.DataFrame:
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    df = pd.read_csv(file_path, sep="\t", skiprows=skiprows)

    return df