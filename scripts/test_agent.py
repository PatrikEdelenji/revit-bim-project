from revit_bim_project.ai.agent import answer_bim_question


def main():
    questions = [
        "Which floor has the most area?",
        "What are the largest rooms?",
        "Are there any suspicious rooms?",
        "Give me a BIM summary.",
        "What materials are used?",
    ]

    for question in questions:
        print("=" * 80)
        print(f"Question: {question}")
        print()
        print(answer_bim_question(question))
        print()


if __name__ == "__main__":
    main()