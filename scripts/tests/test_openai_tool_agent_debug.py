from revit_bim_project.ai.agents.openai_tool_agent import (
    answer_bim_question_with_tool_calling_debug,
)


def main():
    question = "Are there any suspicious rooms?"

    result = answer_bim_question_with_tool_calling_debug(question)

    print("Question:")
    print(question)

    print("\nAnswer:")
    print(result["answer"])

    print("\nTool calls:")
    for tool_call in result["tool_calls"]:
        print(f"- {tool_call['tool_name']} with arguments {tool_call['arguments']}")

    print(f"\nElapsed time: {result['elapsed_seconds']:.2f} seconds")


if __name__ == "__main__":
    main()