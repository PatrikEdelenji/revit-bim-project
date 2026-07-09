from revit_bim_project.ai.embedding_rag import retrieve_bim_rule_context


def main():
    queries = [
        "What metadata should BIM rooms have?",
        "Which rooms should be manually reviewed?",
        "What does Unknown material mean?",
    ]

    for query in queries:
        print("=" * 80)
        print(f"Query: {query}")

        results = retrieve_bim_rule_context(query=query, k=2)

        for index, result in enumerate(results, start=1):
            print(f"\nResult {index}")
            print(f"Source: {result['metadata'].get('source')}")
            print(result["content"][:700])


if __name__ == "__main__":
    main()