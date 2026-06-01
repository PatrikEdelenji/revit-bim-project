import pandas as pd
from sklearn.ensemble import IsolationForest


def detect_room_anomalies(df: pd.DataFrame) -> pd.DataFrame:
    """
    Detect anomalies in room data using Isolation Forest.
    """

    features = df[["area_m2", "volume_m3"]]

    model = IsolationForest(
        n_estimators=100,
        contamination=0.2,
        random_state=42,
    )

    df = df.copy()
    df["anomaly_score"] = model.fit_predict(features)

    anomalies = df[df["anomaly_score"] == -1]

    return anomalies