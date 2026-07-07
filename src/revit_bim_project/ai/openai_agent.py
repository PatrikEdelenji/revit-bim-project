import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from revit_bim_project.ai.tools import (
    area_by_floor_tool,
    material_summary_tool,
    largest_rooms_tool,
    anomalies_tool,
)


load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
model_name = os.getenv("OPENAI_MODEL", "gpt-5.4-mini")

if not api_key:
    raise ValueError(
        "OPENAI_API_KEY is missing. Add it to your .env file."
    )

client = OpenAI(api_key=api_key)


def answer_bim_question_with_openai(question: str) -> str:
    tool_name, tool_result = _select_tool(question)

    prompt = f"""
                You are a BIM data quality assistant.

                The user asked:
                {question}

                The selected BIM analytics tool was:
                {tool_name}

                The tool returned this JSON data:
                {json.dumps(tool_result, indent=2)}

                Important domain rules:
                - The anomaly detection uses Isolation Forest.
                - In the anomaly_score field, -1 means the room was detected as an anomaly.
                - In the anomaly_score field, 1 means the room was detected as normal.
                - Do not say that -1 means missing or undefined.
                - If material is "Unknown", explain that the source BIM data is missing material information.
                - Use only the provided tool result.
                - Do not invent values.
                - Round area and volume values to 2 decimal places.
                - Do not offer extra follow-up actions at the end.
                - Write the answer clearly for a BIM engineer or project manager.
                """

    response = client.responses.create(
        model=model_name,
        input=prompt,
    )

    return response.output_text


def _select_tool(question: str) -> tuple[str, list[dict]]:
    question_lower = question.lower()

    if any(word in question_lower for word in ["largest", "biggest", "large rooms"]):
        return "largest_rooms_tool", largest_rooms_tool(limit=5)

    if any(word in question_lower for word in ["anomaly", "anomalies", "suspicious", "unusual", "review"]):
        return "anomalies_tool", anomalies_tool()

    if any(word in question_lower for word in ["material", "materials"]):
        return "material_summary_tool", material_summary_tool()

    if any(word in question_lower for word in ["summary", "report", "overview"]):
        return "bim_summary", _build_summary_data()

    if any(word in question_lower for word in ["floor", "level", "area"]):
        return "area_by_floor_tool", area_by_floor_tool()

    return "bim_summary", _build_summary_data()


def _build_summary_data() -> list[dict]:
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


def generate_bim_quality_report() -> str:
    """
    Generate a structured BIM quality report using multiple BIM analytics tools.
    """

    floors = area_by_floor_tool()
    largest_rooms = largest_rooms_tool(limit=5)
    anomalies = anomalies_tool()
    materials = material_summary_tool()

    report_data = {
        "area_by_floor": floors,
        "largest_rooms": largest_rooms,
        "detected_anomalies": anomalies,
        "material_summary": materials,
    }

    prompt = f"""
You are a BIM data quality assistant.

Generate a professional BIM Quality Report using only the provided BIM analytics data.

BIM analytics data:
{json.dumps(report_data, indent=2)}

Important domain rules:
- The anomaly detection uses Isolation Forest.
- In the anomaly_score field, -1 means the room was detected as an anomaly.
- Do not say that -1 means missing or undefined.
- If material is "Unknown", explain that the source BIM data is missing material information.
- Use only the provided data.
- Do not invent values.
- Round area and volume values to 2 decimal places.
- Write clearly for a BIM engineer, project manager, or technical reviewer.

Structure the report with these sections:
1. Executive Summary
2. Building Area Overview
3. Largest Rooms
4. Detected Anomalies
5. Missing or Weak Metadata
6. Recommended Manual Checks
7. Conclusion
"""

    response = client.responses.create(
        model=model_name,
        input=prompt,
    )

    return response.output_text