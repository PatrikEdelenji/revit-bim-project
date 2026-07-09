from typing import Any, TypedDict

from langgraph.graph import StateGraph, START, END

from revit_bim_project.ai.langchain_agent import answer_bim_question_with_langchain


class BIMGraphState(TypedDict, total=False):
    question: str
    conversation_history: list[dict]
    prepared_question: str
    agent_result: dict
    answer: str
    tool_calls: list[dict]
    elapsed_seconds: float | None
    mode: str
    fallback_used: bool
    error: str | None
    model: str | None
    usage: dict | None
    graph: str


def prepare_context_node(state: BIMGraphState) -> BIMGraphState:
    """
    Prepare the current user question and conversation history.
    """

    question = state["question"].strip()
    conversation_history = state.get("conversation_history", [])

    return {
        "prepared_question": question,
        "conversation_history": conversation_history,
    }


def run_langchain_agent_node(state: BIMGraphState) -> BIMGraphState:
    """
    Run the LangChain BIM agent inside the LangGraph workflow.
    """

    result = answer_bim_question_with_langchain(
        question=state["prepared_question"],
        conversation_history=state.get("conversation_history", []),
    )

    return {
        "agent_result": result,
    }


def finalize_response_node(state: BIMGraphState) -> BIMGraphState:
    """
    Flatten the LangChain agent result into the final graph response.
    """

    result = state["agent_result"]

    return {
        "answer": result["answer"],
        "tool_calls": result.get("tool_calls", []),
        "elapsed_seconds": result.get("elapsed_seconds"),
        "mode": "langgraph_langchain_agent",
        "fallback_used": result.get("fallback_used", False),
        "error": result.get("error"),
        "model": result.get("model"),
        "usage": result.get("usage"),
        "graph": "bim_langgraph_workflow",
    }


def build_bim_langgraph_workflow():
    graph = StateGraph(BIMGraphState)

    graph.add_node("prepare_context", prepare_context_node)
    graph.add_node("run_langchain_agent", run_langchain_agent_node)
    graph.add_node("finalize_response", finalize_response_node)

    graph.add_edge(START, "prepare_context")
    graph.add_edge("prepare_context", "run_langchain_agent")
    graph.add_edge("run_langchain_agent", "finalize_response")
    graph.add_edge("finalize_response", END)

    return graph.compile()


bim_langgraph_workflow = build_bim_langgraph_workflow()


def answer_bim_question_with_langgraph(
    question: str,
    conversation_history: list[dict] | None = None,
) -> dict[str, Any]:
    """
    Answer a BIM question using a LangGraph workflow around the LangChain agent.
    """

    result = bim_langgraph_workflow.invoke(
        {
            "question": question,
            "conversation_history": conversation_history or [],
        }
    )

    return {
        "answer": result["answer"],
        "tool_calls": result.get("tool_calls", []),
        "elapsed_seconds": result.get("elapsed_seconds"),
        "mode": result.get("mode"),
        "fallback_used": result.get("fallback_used", False),
        "error": result.get("error"),
        "model": result.get("model"),
        "usage": result.get("usage"),
        "graph": result.get("graph"),
    }