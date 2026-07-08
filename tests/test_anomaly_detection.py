import pandas as pd

from revit_bim_project.ai.anomaly_detection import detect_room_anomalies


def test_detect_room_anomalies_returns_dataframe():
    df = pd.DataFrame(
        {
            "room_id": ["A", "B", "C", "D", "E"],
            "room_name": ["Room A", "Room B", "Room C", "Room D", "Room E"],
            "floor": ["L1", "L1", "L1", "L1", "L1"],
            "area_m2": [10, 11, 12, 13, 500],
            "volume_m3": [30, 32, 35, 36, 2000],
            "material": ["Unknown"] * 5,
            "has_window": [False] * 5,
        }
    )

    anomalies = detect_room_anomalies(df)

    assert isinstance(anomalies, pd.DataFrame)
    assert "anomaly_score" in anomalies.columns


def test_detect_room_anomalies_requires_area_and_volume():
    df = pd.DataFrame(
        {
            "room_id": ["A"],
            "room_name": ["Room A"],
        }
    )

    try:
        detect_room_anomalies(df)
    except ValueError:
        assert True
    else:
        assert False, "Expected ValueError when area_m2 and volume_m3 are missing"