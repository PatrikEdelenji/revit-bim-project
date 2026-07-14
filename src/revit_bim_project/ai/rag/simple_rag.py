from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[4]
BIM_RULES_PATH = PROJECT_ROOT / "docs" / "bim_rules" / "bim_room_quality_rules.md"


def load_bim_quality_rules() -> str:
    """
    Load BIM quality rules from the local Markdown knowledge base.
    """

    if not BIM_RULES_PATH.exists():
        raise FileNotFoundError(f"BIM rules file not found: {BIM_RULES_PATH}")

    return BIM_RULES_PATH.read_text(encoding="utf-8")