from src.ingestion.load_rooms import load_rooms_csv


def main():
    df = load_rooms_csv("data/raw/rooms.csv")

    print("Rooms data loaded successfully")
    print(df.head())
    print(f"\nRows: {len(df)}")
    print(f"Columns: {list(df.columns)}")


if __name__ == "__main__":
    main()