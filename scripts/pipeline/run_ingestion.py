from revit_bim_project.ingestion.load_rooms import load_rooms_csv
from revit_bim_project.transformation.clean_rooms import clean_rooms
from revit_bim_project.storage.save_rooms import save_rooms_parquet
from revit_bim_project.transformation.map_revit_rooms import map_revit_rooms
from revit_bim_project.config.paths import RAW_ROOMS_PATH, PROCESSED_ROOMS_PATH


def main():

    #raw_df = load_rooms_csv("RAW_ROOMS_PATH", skiprows=1) <- use this if you export with "Export title - ON"
    raw_df = load_rooms_csv(RAW_ROOMS_PATH)

    mapped_df = map_revit_rooms(raw_df)
    clean_df = clean_rooms(mapped_df)

    output_path = PROCESSED_ROOMS_PATH
    save_rooms_parquet(clean_df, output_path)

    print("Rooms pipeline completed successfully")
    print(f"Rows before cleaning: {len(raw_df)}")
    print(f"Rows after cleaning: {len(clean_df)}")
    print(f"Saved to: {output_path}")


if __name__ == "__main__":
    main()