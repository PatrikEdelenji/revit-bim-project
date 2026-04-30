import pandas as pd
from src.ai.anomaly_detection import detect_room_anomalies


def main():
    df = pd.read_parquet("data/processed/rooms.parquet")

    anomalies = detect_room_anomalies(df)

    print("\nAnomalies detected:")
    print(anomalies)


if __name__ == "__main__":
    main()