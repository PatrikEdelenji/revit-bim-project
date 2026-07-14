try:
    from revit_bim_project.analytics.room_metrics import (
        get_total_area_by_floor,
        get_material_summary,
        get_largest_rooms,
    )
except ImportError:  # pragma: no cover - optional dependency guard
    get_total_area_by_floor = None
    get_material_summary = None
    get_largest_rooms = None

from revit_bim_project.ai.ml import detect_room_anomalies
from revit_bim_project.config.paths import PROCESSED_ROOMS_PATH

try:
    from revit_bim_project.storage.load_processed import load_rooms_parquet
except ImportError:  # pragma: no cover - optional dependency guard
    load_rooms_parquet = None


def area_by_floor_tool() -> list[dict]:
    if get_total_area_by_floor is None:
        raise ImportError("Analytics dependencies are not installed. Install the project dependencies to use BIM analytics tools.")
    result = get_total_area_by_floor(PROCESSED_ROOMS_PATH)
    return result.to_dict(orient="records")


def material_summary_tool() -> list[dict]:
    if get_material_summary is None:
        raise ImportError("Analytics dependencies are not installed. Install the project dependencies to use BIM analytics tools.")
    result = get_material_summary(PROCESSED_ROOMS_PATH)
    return result.to_dict(orient="records")


def largest_rooms_tool(limit: int = 5) -> list[dict]:
    if get_largest_rooms is None:
        raise ImportError("Analytics dependencies are not installed. Install the project dependencies to use BIM analytics tools.")
    result = get_largest_rooms(PROCESSED_ROOMS_PATH, limit=limit)
    return result.to_dict(orient="records")


def anomalies_tool() -> list[dict]:
    if load_rooms_parquet is None:
        raise ImportError("Pandas-backed storage dependencies are not installed. Install the project data dependencies to use anomaly tools.")
    rooms_df = load_rooms_parquet(PROCESSED_ROOMS_PATH)
    result = detect_room_anomalies(rooms_df)
    return result.to_dict(orient="records")


def query_rooms_tool(
    sort_by: str = "area_m2",
    ascending: bool = False,
    limit: int = 5,
    floor: str | None = None,
    material: str | None = None,
    has_window: bool | None = None,
) -> list[dict]:
    """
    Query BIM rooms with optional sorting, filtering, and limiting.
    """

    if load_rooms_parquet is None:
        raise ImportError("Pandas-backed storage dependencies are not installed. Install the project data dependencies to use room query tools.")
    rooms_df = load_rooms_parquet(PROCESSED_ROOMS_PATH)

    allowed_sort_columns = ["area_m2", "volume_m3"]

    if sort_by not in allowed_sort_columns:
        raise ValueError(
            f"Unsupported sort column: {sort_by}. "
            f"Allowed values are: {allowed_sort_columns}"
        )

    if floor is not None:
        rooms_df = rooms_df[rooms_df["floor"].str.lower() == floor.lower()]

    if material is not None:
        rooms_df = rooms_df[rooms_df["material"].str.lower() == material.lower()]

    if has_window is not None:
        rooms_df = rooms_df[rooms_df["has_window"] == has_window]

    result = rooms_df.sort_values(sort_by, ascending=ascending).head(limit)

    return result.to_dict(orient="records")


def bim_summary_tool() -> list[dict]:
    floors = area_by_floor_tool()
    largest_rooms = largest_rooms_tool(limit=3)
    anomalies = anomalies_tool()
    materials = material_summary_tool()

    total_area = sum(floor["total_area_m2"] for floor in floors)
    total_rooms = sum(floor["room_count"] for floor in floors)
    top_floor = max(floors, key=lambda x: x["total_area_m2"]) if floors else None

    return [
        {
            "total_rooms": total_rooms,
            "total_area_m2": total_area,
            "number_of_floors_or_levels": len(floors),
            "floor_with_largest_total_area": top_floor,
            "detected_anomaly_count": len(anomalies),
            "largest_rooms": largest_rooms,
            "material_summary": materials,
        }
    ]
