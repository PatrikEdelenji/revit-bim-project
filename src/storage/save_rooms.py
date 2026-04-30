from pathlib import Path
import pandas as pd


def save_rooms_parquet(df: pd.DataFrame, output_path: str | Path) -> None:
    """
    Save cleaned room data as a Parquet file.
    """

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    df.to_parquet(output_path, index=False)