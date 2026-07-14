from revit_bim_project.ai.rag.embedding_rag import build_bim_rules_vectorstore


def main():
    vectorstore = build_bim_rules_vectorstore()

    print("BIM rules vector store created successfully.")
    print(vectorstore)


if __name__ == "__main__":
    main()