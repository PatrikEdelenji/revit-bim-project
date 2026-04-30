from pathlib import Path
import pandas as pd


def load_rooms_csv(file_path: str | Path) -> pd.DataFrame:
    """
    Load room data exported from Revit or a sample CSV file.
    """

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    df = pd.read_csv(file_path)

    return df