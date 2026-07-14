from scripts.run_ingestion import main as run_ingestion
from scripts.run_analytics import main as run_analytics
from scripts.run_anomaly_detection import main as run_anomaly_detection


def main():
    print("Starting full pipeline...")
    run_ingestion()
    run_analytics()
    run_anomaly_detection()
    print("Pipeline completed successfully.")

if __name__ == "__main__":
    main()