from revit_bim_project.analytics.room_metrics import (
    get_total_area_by_floor,
    get_material_summary,
    get_largest_rooms,
)
from revit_bim_project.ai.anomaly_detection import detect_room_anomalies
from revit_bim_project.config.paths import PROCESSED_ROOMS_PATH
from revit_bim_project.storage.load_processed import load_rooms_parquet
from revit_bim_project.ai.rag import load_bim_quality_rules

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


def bim_quality_rules_tool() -> list[dict]:
    """
    Return BIM room quality rules from the local Markdown knowledge base.

    This tool is useful when the user asks specifically about the rules,
    standards, requirements, or checklist being used.
    """

    rules = load_bim_quality_rules()

    return [
        {
            "document": "bim_room_quality_rules.md",
            "content": rules,
        }
    ]


def bim_quality_review_tool() -> list[dict]:
    """
    Return BIM quality rules together with actual BIM analytics data.

    This tool is useful when the user asks about BIM quality,
    missing metadata, standards, rules, or manual review.
    """

    rules = load_bim_quality_rules()
    summary = bim_summary_tool()
    anomalies = anomalies_tool()
    materials = material_summary_tool()

    return [
        {
            "rules_document": "bim_room_quality_rules.md",
            "rules": rules,
            "bim_summary": summary,
            "detected_anomalies": anomalies,
            "material_summary": materials,
        }
    ]