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