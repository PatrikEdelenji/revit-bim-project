from revit_bim_project.analytics.room_metrics import (
    get_total_area_by_floor,
    get_material_summary,
    get_largest_rooms,
)
from revit_bim_project.ai.anomaly_detection import detect_room_anomalies
from revit_bim_project.config.paths import PROCESSED_ROOMS_PATH
from revit_bim_project.storage.load_processed import load_rooms_parquet


def area_by_floor_tool() -> list[dict]:
    result = get_total_area_by_floor(PROCESSED_ROOMS_PATH)
    return result.to_dict(orient="records")


def material_summary_tool() -> list[dict]:
    result = get_material_summary(PROCESSED_ROOMS_PATH)
    return result.to_dict(orient="records")


def largest_rooms_tool(limit: int = 5) -> list[dict]:
    result = get_largest_rooms(PROCESSED_ROOMS_PATH, limit=limit)
    return result.to_dict(orient="records")


def anomalies_tool() -> list[dict]:
    rooms_df = load_rooms_parquet(PROCESSED_ROOMS_PATH)
    result = detect_room_anomalies(rooms_df)
    return result.to_dict(orient="records")