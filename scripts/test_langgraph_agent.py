from revit_bim_project.ai.langgraph_agent import answer_bim_question_with_langgraph


def main():
    questions = [
        "What is the smallest room?",
        "Does this BIM model have missing metadata?",
        "Which floor has the most area?",
    ]

    for question in questions:
        print("=" * 80)
        print(f"Question: {question}")
        print()

        result = answer_bim_question_with_langgraph(question)

        print(result["answer"])

        print()
        print(f"Graph: {result['graph']}")
        print(f"Mode: {result['mode']}")
        print(f"Model: {result['model']}")
        print(f"Elapsed: {result['elapsed_seconds']:.2f} seconds")

        print("\nTools:")
        for tool_call in result["tool_calls"]:
            print(f"- {tool_call['tool_name']}: {tool_call['arguments']}")


if __name__ == "__main__":
    main()