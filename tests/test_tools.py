from revit_bim_project.ai.tools import (
    area_by_floor_tool,
    material_summary_tool,
    largest_rooms_tool,
    anomalies_tool,
    bim_summary_tool,
    bim_quality_review_tool,
)


def test_area_by_floor_tool_returns_data():
    result = area_by_floor_tool()

    assert isinstance(result, list)
    assert len(result) > 0
    assert "floor" in result[0]
    assert "total_area_m2" in result[0]
    assert "room_count" in result[0]


def test_material_summary_tool_returns_data():
    result = material_summary_tool()

    assert isinstance(result, list)
    assert len(result) > 0
    assert "material" in result[0]
    assert "room_count" in result[0]
    assert "total_area_m2" in result[0]


def test_largest_rooms_tool_returns_limited_results():
    result = largest_rooms_tool(limit=3)

    assert isinstance(result, list)
    assert len(result) <= 3

    if result:
        assert "room_id" in result[0]
        assert "room_name" in result[0]
        assert "area_m2" in result[0]


def test_anomalies_tool_returns_list():
    result = anomalies_tool()

    assert isinstance(result, list)

    if result:
        assert "room_id" in result[0]
        assert "anomaly_score" in result[0]


def test_bim_summary_tool_returns_summary():
    result = bim_summary_tool()

    assert isinstance(result, list)
    assert len(result) == 1

    summary = result[0]

    assert "total_rooms" in summary
    assert "total_area_m2" in summary
    assert "detected_anomaly_count" in summary
    assert "largest_rooms" in summary
    assert "material_summary" in summary


def test_bim_quality_review_tool_returns_rules_and_data():
    result = bim_quality_review_tool()

    assert isinstance(result, list)
    assert len(result) == 1

    review = result[0]

    assert "rules" in review
    assert "bim_summary" in review
    assert "detected_anomalies" in review
    assert "material_summary" in review