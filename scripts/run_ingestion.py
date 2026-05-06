from src.ingestion.load_revit_api_export import load_revit_rooms_json
from src.transformation.clean_rooms import clean_rooms
from src.storage.save_rooms import save_rooms_parquet


def main():
    raw_df = load_revit_rooms_json("data/raw/revit_rooms_api_export.json")

    clean_df = clean_rooms(raw_df)

    output_path = "data/processed/rooms.parquet"
    save_rooms_parquet(clean_df, output_path)

    print("Rooms API pipeline completed successfully")
    print(f"Rows before cleaning: {len(raw_df)}")
    print(f"Rows after cleaning: {len(clean_df)}")
    print(f"Saved to: {output_path}")


if __name__ == "__main__":
    main()