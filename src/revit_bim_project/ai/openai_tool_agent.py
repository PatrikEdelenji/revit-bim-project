import json
import os
import time
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI

from revit_bim_project.ai.tools import (
    area_by_floor_tool,
    largest_rooms_tool,
    anomalies_tool,
    material_summary_tool,
    bim_summary_tool,
    bim_quality_rules_tool,
    bim_quality_review_tool,
)


PROJECT_ROOT = Path(__file__).resolve().parents[3]
ENV_PATH = PROJECT_ROOT / ".env"

load_dotenv(dotenv_path=ENV_PATH)

api_key = os.getenv("OPENAI_API_KEY")
model_name = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

if not api_key:
    raise ValueError(f"OPENAI_API_KEY is missing. Expected .env file at: {ENV_PATH}")

client = OpenAI(api_key=api_key)


TOOL_FUNCTIONS = {
    "area_by_floor_tool": area_by_floor_tool,
    "largest_rooms_tool": largest_rooms_tool,
    "anomalies_tool": anomalies_tool,
    "material_summary_tool": material_summary_tool,
    "bim_summary_tool": bim_summary_tool,
    # "bim_quality_rules_tool": bim_quality_rules_tool,
    "bim_quality_review_tool": bim_quality_review_tool,
}

TOOLS = [
    {
        "type": "function",
        "name": "area_by_floor_tool",
        "description": "Returns total BIM room area grouped by floor or level.",
        "parameters": {
            "type": "object",
            "properties": {},
            "additionalProperties": False,
        },
    },
    {
        "type": "function",
        "name": "largest_rooms_tool",
        "description": "Returns the largest rooms in the BIM model by area.",
        "parameters": {
            "type": "object",
            "properties": {
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of largest rooms to return.",
                    "default": 5,
                }
            },
            "additionalProperties": False,
        },
    },
    {
        "type": "function",
        "name": "anomalies_tool",
        "description": "Returns rooms detected as anomalies using Isolation Forest based on area and volume.",
        "parameters": {
            "type": "object",
            "properties": {},
            "additionalProperties": False,
        },
    },
    {
        "type": "function",
        "name": "material_summary_tool",
        "description": "Returns BIM room material summary, including room count and total area per material.",
        "parameters": {
            "type": "object",
            "properties": {},
            "additionalProperties": False,
        },
    },
    {
        "type": "function",
        "name": "bim_summary_tool",
        "description": "Returns a general BIM model summary including total rooms, total area, top floor, largest rooms, anomalies, and material summary.",
        "parameters": {
            "type": "object",
            "properties": {},
            "additionalProperties": False,
        },
    },
    # {
    #     "type": "function",
    #     "name": "bim_quality_rules_tool",
    #     "description": (
    #         "Returns only the written BIM quality rules/checklist. "
    #         "Use this only when the user specifically asks to see, list, or explain the rules themselves. "
    #         "Do not use this to evaluate the current BIM model."
    #     ),
    #     "parameters": {
    #         "type": "object",
    #         "properties": {},
    #         "additionalProperties": False,
    #     },
    # },
    {
        "type": "function",
        "name": "bim_quality_review_tool",
        "description": (
            "Evaluates the current BIM model against BIM quality rules. "
            "Returns both the BIM quality rules and actual BIM analytics data, including model summary, "
            "detected anomalies, and material metadata. "
            "Use this for questions about missing metadata, model quality, manual review, standards compliance, "
            "whether the BIM model follows rules, or which rooms should be reviewed."
        ),
        "parameters": {
            "type": "object",
            "properties": {},
            "additionalProperties": False,
        },
    },
]


SYSTEM_PROMPT = """
You are a BIM data quality assistant.

You answer questions about processed Revit/BIM room data by using available tools.

Important rules:
- Use tools to get BIM facts. Do not guess values.
- The anomaly detection uses Isolation Forest.
- In anomaly_score, -1 means the room was detected as an anomaly.
- In anomaly_score, 1 means the room was detected as normal.
- Do not say that -1 means missing or undefined.
- If material is "Unknown", explain that the BIM source data is missing material information.
- Round area and volume values to 2 decimal places.
- Write clearly for a BIM engineer or project manager.
- Do not offer unnecessary follow-up actions at the end.
- If the user asks about standards, rules, requirements, quality checks, compliance, or whether the BIM data is good enough, use the BIM quality rules tool.
- When comparing BIM data against rules, clearly separate actual BIM data findings from rule-based recommendations.
- If the user asks whether the current BIM model has missing metadata, quality issues, compliance issues, or rooms needing manual review, you must use bim_quality_review_tool.
- Use bim_quality_review_tool whenever the question requires both BIM rules and actual BIM model data.
- Use bim_quality_rules_tool only if the user specifically asks to see or explain the written rules/checklist itself.
- Do not answer model-quality questions using only bim_quality_rules_tool.
"""


def answer_bim_question_with_tool_calling(question: str) -> str:
    """
    OpenAI tool-calling BIM agent.

    The model chooses which BIM tool to call.
    Python executes the tool.
    The model writes the final answer using the tool output.
    """

    first_response = client.responses.create(
        model=model_name,
        input=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": question,
            },
        ],
        tools=TOOLS,
    )

    tool_outputs = _execute_tool_calls(first_response)

    if not tool_outputs:
        return first_response.output_text

    second_input: list[dict[str, Any]] = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": question,
        },
    ]

    for tool_output in tool_outputs:
        second_input.append(
            {
                "role": "user",
                "content": (
                    f"Tool called: {tool_output['tool_name']}\n"
                    f"Tool result JSON:\n{json.dumps(tool_output['result'], indent=2)}"
                ),
            }
        )

    final_response = client.responses.create(
        model=model_name,
        input=second_input,
    )

    return final_response.output_text


def answer_bim_question_with_tool_calling_debug(question: str) -> dict:
    """
    OpenAI tool-calling BIM agent with debug metadata.

    Returns:
    - final answer
    - selected tool calls
    - execution time
    """

    start_time = time.perf_counter()

    first_response = client.responses.create(
        model=model_name,
        input=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": question,
            },
        ],
        tools=TOOLS,
    )

    tool_outputs = _execute_tool_calls(first_response)

    if not tool_outputs:
        elapsed_seconds = time.perf_counter() - start_time
        return {
            "answer": first_response.output_text,
            "tool_calls": [],
            "elapsed_seconds": elapsed_seconds,
        }

    second_input: list[dict[str, Any]] = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": question,
        },
    ]

    for tool_output in tool_outputs:
        second_input.append(
            {
                "role": "user",
                "content": (
                    f"Tool called: {tool_output['tool_name']}\n"
                    f"Tool arguments:\n{json.dumps(tool_output['arguments'], indent=2)}\n"
                    f"Tool result JSON:\n{json.dumps(tool_output['result'], indent=2)}"
                ),
            }
        )

    final_response = client.responses.create(
        model=model_name,
        input=second_input,
    )

    elapsed_seconds = time.perf_counter() - start_time

    return {
        "answer": final_response.output_text,
        "tool_calls": tool_outputs,
        "elapsed_seconds": elapsed_seconds,
    }


def _execute_tool_calls(response) -> list[dict[str, Any]]:
    tool_outputs = []

    for item in response.output:
        if item.type != "function_call":
            continue

        tool_name = item.name
        raw_arguments = item.arguments or "{}"
        arguments = json.loads(raw_arguments)

        if tool_name not in TOOL_FUNCTIONS:
            raise ValueError(f"Unknown tool requested by model: {tool_name}")

        if tool_name == "largest_rooms_tool":
            limit = arguments.get("limit", 5)
            result = TOOL_FUNCTIONS[tool_name](limit=limit)
        else:
            result = TOOL_FUNCTIONS[tool_name]()

        tool_outputs.append(
            {
                "tool_name": tool_name,
                "arguments": arguments,
                "result": result,
            }
        )

    return tool_outputs