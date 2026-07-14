import json
from pathlib import Path

from revit_bim_project.ai.agents.langgraph_agent import answer_bim_question_with_langgraph


PROJECT_ROOT = Path(__file__).resolve().parents[2]
EVAL_FILE = PROJECT_ROOT / "eval" / "bim_agent_eval.json"


def main():
    with open(EVAL_FILE, "r", encoding="utf-8") as file:
        eval_cases = json.load(file)

    passed = 0

    for index, case in enumerate(eval_cases, start=1):
        question = case["question"]
        expected_contains = case.get("expected_contains", [])

        print("=" * 80)
        print(f"Case {index}: {question}")

        result = answer_bim_question_with_langgraph(question)

        answer = result["answer"]
        tool_calls = result.get("tool_calls", [])

        selected_tools = [
            tool_call["tool_name"]
            for tool_call in tool_calls
        ]

        normalized_answer = answer.lower().replace(",", "")

        contains_passed = all(
            expected.lower().replace(",", "") in normalized_answer
            for expected in expected_contains
        )

        expected_tool = case.get("expected_tool")
        expected_langgraph_tool = _map_expected_tool_name(expected_tool)

        tool_passed = True

        if expected_langgraph_tool:
            tool_passed = expected_langgraph_tool in selected_tools

        case_passed = contains_passed and tool_passed

        if case_passed:
            passed += 1
            print("Result: PASS")
        else:
            print("Result: FAIL")

        print("\nExpected contains:")
        print(expected_contains)

        print("\nExpected tool:")
        print(expected_langgraph_tool)

        print("\nSelected tools:")
        print(selected_tools)

        print("\nGraph:")
        print(result.get("graph"))

        print("\nAnswer:")
        print(answer)

    total = len(eval_cases)
    accuracy = passed / total * 100 if total else 0

    print("=" * 80)
    print(f"Passed {passed}/{total} cases")
    print(f"Accuracy: {accuracy:.1f}%")


def _map_expected_tool_name(expected_tool: str | None) -> str | None:
    if expected_tool is None:
        return None

    mapping = {
        "area_by_floor_tool": "area_by_floor",
        "query_rooms_tool": "query_rooms",
        "largest_rooms_tool": "query_rooms",
        "anomalies_tool": "anomalies",
        "material_summary_tool": "material_summary",
        "bim_summary_tool": "bim_summary",
        "bim_quality_review_tool": "bim_quality_review",
        "bim_rules_retriever_tool": "bim_rules_retriever",
    }

    return mapping.get(expected_tool, expected_tool)


if __name__ == "__main__":
    main()