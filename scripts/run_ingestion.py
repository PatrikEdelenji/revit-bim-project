from src.ingestion.load_rooms import load_rooms_csv
from src.transformation.clean_rooms import clean_rooms
from src.storage.save_rooms import save_rooms_parquet
from src.transformation.map_revit_rooms import map_revit_rooms


def main():
    raw_df = load_rooms_csv("data/raw/revit_rooms_export.txt", skiprows=1)

    mapped_df = map_revit_rooms(raw_df)
    clean_df = clean_rooms(mapped_df)

    output_path = "data/processed/rooms.parquet"
    save_rooms_parquet(clean_df, output_path)

    print("Rooms pipeline completed successfully")
    print(f"Rows before cleaning: {len(raw_df)}")
    print(f"Rows after cleaning: {len(clean_df)}")
    print(f"Saved to: {output_path}")


if __name__ == "__main__":
    main()