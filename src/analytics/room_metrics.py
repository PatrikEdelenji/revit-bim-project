from pathlib import Path
import duckdb
import pandas as pd


def get_total_area_by_floor(parquet_path: str | Path) -> pd.DataFrame:
    query = """
    SELECT
        floor,
        SUM(area_m2) AS total_area_m2,
        COUNT(*) AS room_count
    FROM read_parquet(?)
    GROUP BY floor
    ORDER BY floor
    """

    return duckdb.execute(query, [str(parquet_path)]).df()


def get_material_summary(parquet_path: str | Path) -> pd.DataFrame:
    query = """
    SELECT
        material,
        COUNT(*) AS room_count,
        SUM(area_m2) AS total_area_m2
    FROM read_parquet(?)
    GROUP BY material
    ORDER BY total_area_m2 DESC
    """

    return duckdb.execute(query, [str(parquet_path)]).df()


def get_largest_rooms(parquet_path: str | Path, limit: int = 5) -> pd.DataFrame:
    query = """
    SELECT
        room_id,
        room_name,
        floor,
        area_m2,
        volume_m3,
        material
    FROM read_parquet(?)
    ORDER BY area_m2 DESC
    LIMIT ?
    """

    return duckdb.execute(query, [str(parquet_path), limit]).df()