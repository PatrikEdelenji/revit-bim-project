import json
import os
import time
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI

from revit_bim_project.ai.tools import (
    area_by_floor_tool,
    query_rooms_tool,
    anomalies_tool,
    material_summary_tool,
    bim_summary_tool,
    bim_quality_review_tool,
)


PROJECT_ROOT = Path(__file__).resolve().parents[3]
ENV_PATH = PROJECT_ROOT / ".env"

load_dotenv(dotenv_path=ENV_PATH)

api_key = os.getenv("OPENAI_API_KEY")
model_name = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

if not api_key:
    raise ValueError(f"OPENAI_API_KEY is missing. Expected .env file at: {ENV_PATH}")


SYSTEM_PROMPT = """
You are a BIM data quality assistant.

You answer questions about processed Revit/BIM room data by using available tools.

Important rules:
- Use tools to get BIM facts. Do not guess values.
- If the user asks about largest rooms, smallest rooms, rooms by area, rooms by volume, rooms on a floor, or rooms with filters, use query_rooms.
- If the user asks about missing metadata, quality rules, compliance, or manual review, use bim_quality_review.
- The anomaly detection uses Isolation Forest.
- In anomaly_score, -1 means the room was detected as an anomaly.
- If material is "Unknown", explain that the BIM source data is missing material information.
- Round area and volume values to 2 decimal places.
- Write clearly for a BIM engineer or project manager.
"""


@tool
def area_by_floor() -> str:
    """Return total BIM room area grouped by floor or level."""
    return json.dumps(area_by_floor_tool(), indent=2)


@tool
def query_rooms(
    sort_by: str = "area_m2",
    ascending: bool = False,
    limit: int = 5,
    floor: str | None = None,
    material: str | None = None,
    has_window: bool | None = None,
) -> str:
    """
    Query BIM rooms with flexible sorting, filtering, and limiting.

    Use this for largest rooms, smallest rooms, rooms by volume,
    rooms by area, rooms on a specific floor, rooms with a specific material,
    or rooms with/without windows.
    """
    result = query_rooms_tool(
        sort_by=sort_by,
        ascending=ascending,
        limit=limit,
        floor=floor,
        material=material,
        has_window=has_window,
    )
    return json.dumps(result, indent=2)


@tool
def anomalies() -> str:
    """Return rooms detected as anomalies using Isolation Forest."""
    return json.dumps(anomalies_tool(), indent=2)


@tool
def material_summary() -> str:
    """Return BIM room material summary."""
    return json.dumps(material_summary_tool(), indent=2)


@tool
def bim_summary() -> str:
    """Return a general BIM model summary."""
    return json.dumps(bim_summary_tool(), indent=2)


@tool
def bim_quality_review() -> str:
    """
    Evaluate the current BIM model against BIM quality rules.

    Use this for questions about missing metadata, model quality,
    standards compliance, manual review, or whether the model follows BIM rules.
    """
    return json.dumps(bim_quality_review_tool(), indent=2)


TOOLS = [
    area_by_floor,
    query_rooms,
    anomalies,
    material_summary,
    bim_summary,
    bim_quality_review,
]


model = ChatOpenAI(
    model=model_name,
    api_key=api_key,
)

agent = create_agent(
    model=model,
    tools=TOOLS,
    system_prompt=SYSTEM_PROMPT,
)


def answer_bim_question_with_langchain(
    question: str,
    conversation_history: list[dict] | None = None,
) -> dict[str, Any]:
    """
    Answer a BIM question using a LangChain agent.
    """

    start_time = time.perf_counter()

    messages = []

    if conversation_history:
        for message in conversation_history[-4:]:
            messages.append(
                {
                    "role": "user",
                    "content": message.get("question", ""),
                }
            )
            messages.append(
                {
                    "role": "assistant",
                    "content": message.get("answer", ""),
                }
            )

    messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    result = agent.invoke(
        {
            "messages": messages,
        }
    )

    elapsed_seconds = time.perf_counter() - start_time

    final_message = result["messages"][-1]
    answer = final_message.content

    tool_calls = _extract_langchain_tool_calls(result["messages"])

    return {
        "answer": answer,
        "elapsed_seconds": elapsed_seconds,
        "mode": "langchain_agent",
        "fallback_used": False,
        "error": None,
        "model": model_name,
        "usage": None,
        "tool_calls": tool_calls,
    }


def _extract_langchain_tool_calls(messages: list) -> list[dict]:
    """
    Extract tool-call debug information from LangChain agent messages.
    """

    extracted_tool_calls = []

    for message in messages:
        message_tool_calls = getattr(message, "tool_calls", None)

        if not message_tool_calls:
            continue

        for tool_call in message_tool_calls:
            extracted_tool_calls.append(
                {
                    "tool_name": tool_call.get("name"),
                    "arguments": tool_call.get("args", {}),
                }
            )

    return extracted_tool_calls