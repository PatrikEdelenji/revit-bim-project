from importlib import import_module

__all__ = [
    "answer_bim_question",
    "answer_bim_question_with_openai",
    "answer_bim_question_with_tool_calling",
    "answer_bim_question_with_tool_calling_debug",
    "answer_bim_question_with_langchain",
    "answer_bim_question_with_langgraph",
    "answer_bim_question_safely",
]

_EXPORTS = {
    "answer_bim_question": ".rule_based_agent",
    "answer_bim_question_with_openai": ".openai_explanation_agent",
    "answer_bim_question_with_tool_calling": ".openai_tool_agent",
    "answer_bim_question_with_tool_calling_debug": ".openai_tool_agent",
    "answer_bim_question_with_langchain": ".langchain_agent",
    "answer_bim_question_with_langgraph": ".langgraph_agent",
    "answer_bim_question_safely": ".safe_agent",
}


def __getattr__(name: str):
    if name in _EXPORTS:
        module = import_module(_EXPORTS[name], __name__)
        return getattr(module, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
