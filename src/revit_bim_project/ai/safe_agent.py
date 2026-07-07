from revit_bim_project.ai.agent import answer_bim_question
from revit_bim_project.ai.openai_tool_agent import (
    answer_bim_question_with_tool_calling_debug,
)
from revit_bim_project.utils.logging_utils import get_agent_logger

logger = get_agent_logger()

def answer_bim_question_safely(question: str) -> dict:
    """
    Try OpenAI tool-calling agent first.
    If it fails, fall back to the rule-based local agent.
    """

    try:
        result = answer_bim_question_with_tool_calling_debug(question)

        tool_names = [
            tool_call["tool_name"]
            for tool_call in result["tool_calls"]
        ]

        logger.info(
            "mode=openai_tool_calling | fallback=False | elapsed=%.2fs | question=%r | tools=%s",
            result["elapsed_seconds"],
            question,
            tool_names,
        )

        return {
            "answer": result["answer"],
            "tool_calls": result["tool_calls"],
            "elapsed_seconds": result["elapsed_seconds"],
            "mode": "openai_tool_calling",
            "fallback_used": False,
            "error": None,
        }

    except Exception as error:
        fallback_answer = answer_bim_question(question)

        logger.exception(
            "mode=rule_based_fallback | fallback=True | question=%r | error=%s",
            question,
            str(error),
        )

        return {
            "answer": fallback_answer,
            "tool_calls": [],
            "elapsed_seconds": None,
            "mode": "rule_based_fallback",
            "fallback_used": True,
            "error": str(error),
        }