try:
    import pandas as pd
    from sklearn.ensemble import IsolationForest
except ImportError:  # pragma: no cover - optional dependency guard
    pd = None
    IsolationForest = None


def detect_room_anomalies(df):
    """
    Detect anomalies in room data using Isolation Forest.
    """

    if pd is None or IsolationForest is None:
        raise ImportError("pandas and scikit-learn are required to run anomaly detection.")

    required_columns = ["area_m2", "volume_m3"]

    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns for anomaly detection: {missing_columns}")

    df = df.copy()

    features = df[required_columns].dropna()

    if features.empty:
        return df.iloc[0:0]

    model = IsolationForest(
        n_estimators=100,
        contamination=0.1,
        random_state=42,
    )

    predictions = model.fit_predict(features)

    df.loc[features.index, "anomaly_score"] = predictions

    anomalies = df[df["anomaly_score"] == -1]

    return anomalies