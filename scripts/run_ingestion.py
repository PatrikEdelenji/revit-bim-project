from src.ingestion.load_rooms import load_rooms_csv
from src.transformation.clean_rooms import clean_rooms


def main():
    raw_df = load_rooms_csv("data/raw/rooms.csv")
    clean_df = clean_rooms(raw_df)

    print("Rooms data loaded and cleaned successfully")
    print(clean_df.head())
    print(f"\nRows before cleaning: {len(raw_df)}")
    print(f"Rows after cleaning: {len(clean_df)}")
    print(f"Columns: {list(clean_df.columns)}")


if __name__ == "__main__":
    main()