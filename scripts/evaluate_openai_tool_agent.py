import json
from pathlib import Path

from revit_bim_project.ai.openai_tool_agent import (
    answer_bim_question_with_tool_calling_debug,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
EVAL_FILE = PROJECT_ROOT / "eval" / "bim_agent_eval.json"


def main():
    eval_cases = json.loads(EVAL_FILE.read_text(encoding="utf-8"))

    total = len(eval_cases)
    passed = 0

    print(f"Running {total} BIM agent evaluation cases...\n")

    for index, case in enumerate(eval_cases, start=1):
        question = case["question"]
        expected_tool = case["expected_tool"]
        expected_contains = case["expected_contains"]

        result = answer_bim_question_with_tool_calling_debug(question)

        answer = result["answer"]
        selected_tools = [tool_call["tool_name"] for tool_call in result["tool_calls"]]

        tool_passed = expected_tool in selected_tools
        content_passed = all(
            expected_text.lower() in answer.lower()
            for expected_text in expected_contains
        )

        case_passed = tool_passed and content_passed

        if case_passed:
            passed += 1

        print("=" * 80)
        print(f"Case {index}: {question}")
        print(f"Expected tool: {expected_tool}")
        print(f"Selected tools: {selected_tools}")
        print(f"Tool passed: {tool_passed}")
        print(f"Content passed: {content_passed}")
        print(f"Elapsed: {result['elapsed_seconds']:.2f} seconds")
        print(f"Result: {'PASSED' if case_passed else 'FAILED'}")

        if not case_passed:
            print("\nAnswer:")
            print(answer)

    print("=" * 80)
    print(f"Passed {passed}/{total} cases")
    print(f"Accuracy: {(passed / total) * 100:.1f}%")


if __name__ == "__main__":
    main()