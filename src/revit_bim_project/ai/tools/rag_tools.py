from revit_bim_project.ai.rag import load_bim_quality_rules, retrieve_bim_rule_context


def bim_quality_rules_tool() -> list[dict]:
    """
    Return BIM room quality rules from the local Markdown knowledge base.
    """

    rules = load_bim_quality_rules()

    return [{"document": "bim_room_quality_rules.md", "content": rules}]


def bim_quality_review_tool() -> list[dict]:
    """
    Return BIM quality rules together with actual BIM analytics data.
    """

    from revit_bim_project.ai.tools.bim_tools import (
        anomalies_tool,
        area_by_floor_tool,
        bim_summary_tool,
        material_summary_tool,
    )

    rules = load_bim_quality_rules()
    summary = bim_summary_tool()
    anomalies = anomalies_tool()
    materials = material_summary_tool()

    return [
        {
            "rules_document": "bim_room_quality_rules.md",
            "rules": rules,
            "bim_summary": summary,
            "detected_anomalies": anomalies,
            "material_summary": materials,
        }
    ]


def bim_rules_retriever_tool(query: str, k: int = 3) -> list[dict]:
    """
    Retrieve relevant BIM quality rule chunks using embedding-based semantic search.
    """

    return retrieve_bim_rule_context(query=query, k=k)
