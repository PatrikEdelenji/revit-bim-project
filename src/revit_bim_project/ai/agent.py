from revit_bim_project.ai.tools import (
    area_by_floor_tool,
    material_summary_tool,
    largest_rooms_tool,
    anomalies_tool,
)


def answer_bim_question(question: str) -> str:
    question_lower = question.lower()

    if any(word in question_lower for word in ["largest", "biggest", "large rooms"]):
        return _answer_largest_rooms()

    if any(word in question_lower for word in ["anomaly", "anomalies", "suspicious", "unusual", "review"]):
        return _answer_anomalies()

    if any(word in question_lower for word in ["material", "materials"]):
        return _answer_materials()

    if any(word in question_lower for word in ["summary", "report", "overview"]):
        return _answer_summary()

    if any(word in question_lower for word in ["floor", "level", "area"]):
        return _answer_area_by_floor()

    return (
        "I can help analyze the BIM model. Try asking about total area by floor, "
        "largest rooms, anomalies, suspicious rooms, materials, or a building summary."
    )


def _answer_area_by_floor() -> str:
    floors = area_by_floor_tool()

    if not floors:
        return "I could not find area-by-floor data."

    top_floor = max(floors, key=lambda x: x["total_area_m2"])

    lines = [
        "Area by floor:",
        "",
    ]

    for floor in floors:
        lines.append(
            f"- {floor['floor']}: {floor['total_area_m2']:.2f} m² "
            f"across {floor['room_count']} rooms"
        )

    lines.append("")
    lines.append(
        f"The floor with the largest total area is {top_floor['floor']} "
        f"with {top_floor['total_area_m2']:.2f} m²."
    )

    return "\n".join(lines)


def _answer_largest_rooms(limit: int = 5) -> str:
    rooms = largest_rooms_tool(limit=limit)

    if not rooms:
        return "I could not find largest-room data."

    lines = [
        f"Top {len(rooms)} largest rooms:",
        "",
    ]

    for room in rooms:
        lines.append(
            f"- {room['room_id']} — {room['room_name']} on {room['floor']}: "
            f"{room['area_m2']:.2f} m²"
        )

    return "\n".join(lines)


def _answer_anomalies() -> str:
    anomalies = anomalies_tool()

    if not anomalies:
        return "No anomalous rooms were detected in the current BIM data."

    lines = [
        f"I found {len(anomalies)} rooms that may need manual review:",
        "",
    ]

    for room in anomalies:
        lines.append(
            f"- {room['room_id']} — {room['room_name']} on {room['floor']}: "
            f"{room['area_m2']:.2f} m², {room['volume_m3']:.2f} m³"
        )

    lines.append("")
    lines.append(
        "These rooms were flagged because their area and volume patterns are unusual "
        "compared with the rest of the model. A BIM engineer should review room boundaries, "
        "classification, and metadata for these rooms."
    )

    return "\n".join(lines)


def _answer_materials() -> str:
    materials = material_summary_tool()

    if not materials:
        return "I could not find material data."

    lines = [
        "Material summary:",
        "",
    ]

    for material in materials:
        lines.append(
            f"- {material['material']}: {material['room_count']} rooms, "
            f"{material['total_area_m2']:.2f} m²"
        )

    if len(materials) == 1 and materials[0]["material"] == "Unknown":
        lines.append("")
        lines.append(
            "All rooms currently have material set to Unknown, so the Revit export "
            "does not yet provide useful material-level analysis."
        )

    return "\n".join(lines)


def _answer_summary() -> str:
    floors = area_by_floor_tool()
    largest_rooms = largest_rooms_tool(limit=3)
    anomalies = anomalies_tool()
    materials = material_summary_tool()

    total_area = sum(floor["total_area_m2"] for floor in floors)
    total_rooms = sum(floor["room_count"] for floor in floors)
    top_floor = max(floors, key=lambda x: x["total_area_m2"])

    lines = [
        "BIM Model Summary",
        "",
        f"- Total rooms: {total_rooms}",
        f"- Total area: {total_area:.2f} m²",
        f"- Number of floors/levels: {len(floors)}",
        f"- Largest total area: {top_floor['floor']} with {top_floor['total_area_m2']:.2f} m²",
        f"- Detected anomalies: {len(anomalies)}",
        "",
        "Largest rooms:",
    ]

    for room in largest_rooms:
        lines.append(
            f"- {room['room_id']} — {room['room_name']}: {room['area_m2']:.2f} m²"
        )

    if len(materials) == 1 and materials[0]["material"] == "Unknown":
        lines.append("")
        lines.append(
            "Material data is currently unavailable because all rooms are marked as Unknown."
        )

    lines.append("")
    lines.append(
        "Recommended next step: manually review the detected anomalies and improve "
        "the Revit export with richer metadata such as materials, room types, and window data."
    )

    return "\n".join(lines)