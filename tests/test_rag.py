from revit_bim_project.ai.rag.simple_rag import load_bim_quality_rules


def test_load_bim_quality_rules_returns_text():
    rules = load_bim_quality_rules()

    assert isinstance(rules, str)
    assert len(rules) > 0
    assert "BIM" in rules or "Room" in rules