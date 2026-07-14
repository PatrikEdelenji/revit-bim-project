from revit_bim_project.analytics.room_metrics import (
    get_total_area_by_floor,
    get_material_summary,
    get_largest_rooms,
)
from revit_bim_project.config.paths import PROCESSED_ROOMS_PATH


def main():
    parquet_path = PROCESSED_ROOMS_PATH

    print("\nTotal area by floor:")
    print(get_total_area_by_floor(parquet_path))

    print("\nMaterial summary:")
    print(get_material_summary(parquet_path))

    print("\nLargest rooms:")
    print(get_largest_rooms(parquet_path, limit=5))


if __name__ == "__main__":
    main()