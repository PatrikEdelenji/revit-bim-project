import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from revit_bim_project.config.paths import PROJECT_ROOT


ENV_PATH = PROJECT_ROOT / ".env"
RULES_DIR = PROJECT_ROOT / "docs" / "bim_rules"
VECTOR_STORE_DIR = PROJECT_ROOT / "data" / "vectorstores" / "bim_rules_faiss"

load_dotenv(dotenv_path=ENV_PATH)


def load_bim_rule_documents() -> list[Document]:
    """
    Load BIM rule Markdown files as LangChain Documents.
    """

    documents = []

    for file_path in RULES_DIR.glob("*.md"):
        content = file_path.read_text(encoding="utf-8")

        documents.append(
            Document(
                page_content=content,
                metadata={
                    "source": str(file_path.relative_to(PROJECT_ROOT)),
                    "file_name": file_path.name,
                },
            )
        )

    if not documents:
        raise FileNotFoundError(f"No Markdown rule files found in: {RULES_DIR}")

    return documents


def split_documents(documents: list[Document]) -> list[Document]:
    """
    Split long BIM rule documents into smaller retrievable chunks.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=100,
    )

    return splitter.split_documents(documents)


def build_bim_rules_vectorstore() -> FAISS:
    """
    Build and save a FAISS vector store from BIM rule documents.
    """

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError(f"OPENAI_API_KEY is missing. Expected .env at: {ENV_PATH}")

    documents = load_bim_rule_documents()
    chunks = split_documents(documents)

    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        api_key=api_key,
    )

    vectorstore = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings,
    )

    VECTOR_STORE_DIR.mkdir(parents=True, exist_ok=True)
    vectorstore.save_local(str(VECTOR_STORE_DIR))

    return vectorstore


def load_bim_rules_vectorstore() -> FAISS:
    """
    Load the saved FAISS vector store.
    """

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError(f"OPENAI_API_KEY is missing. Expected .env at: {ENV_PATH}")

    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        api_key=api_key,
    )

    if not VECTOR_STORE_DIR.exists():
        return build_bim_rules_vectorstore()

    return FAISS.load_local(
        folder_path=str(VECTOR_STORE_DIR),
        embeddings=embeddings,
        allow_dangerous_deserialization=True,
    )


def retrieve_bim_rule_context(query: str, k: int = 3) -> list[dict]:
    """
    Retrieve the most relevant BIM rule chunks for a question.
    """

    vectorstore = load_bim_rules_vectorstore()

    documents = vectorstore.similarity_search(
        query=query,
        k=k,
    )

    return [
        {
            "content": document.page_content,
            "metadata": document.metadata,
        }
        for document in documents
    ]