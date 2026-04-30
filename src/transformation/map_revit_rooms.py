import pandas as pd


def parse_number_with_unit(value) -> float | None:
    """
    Convert values like '915 SF' or '18,628.13 CF' to float.
    Returns None for empty/NaN values.
    """
    if pd.isna(value):
        return None

    value = str(value).replace(",", "").strip()

    if value == "":
        return None

    return float(value.split()[0])


def map_revit_rooms(df: pd.DataFrame) -> pd.DataFrame:
    """
    Map raw Revit schedule columns to standardized schema.
    """

    df = df.copy()
    df.columns = df.columns.str.strip()

    mapped = df.rename(
        columns={
            "Number": "room_id",
            "Name": "room_name",
            "Level": "floor",
            "Area": "area_raw",
            "Volume": "volume_raw",
        }
    )

    # Remove empty rows from Revit export
    mapped = mapped.dropna(subset=["room_id", "room_name"])

    mapped["area_m2"] = mapped["area_raw"].apply(parse_number_with_unit)
    mapped["volume_m3"] = mapped["volume_raw"].apply(parse_number_with_unit)

    # Temporary placeholders until we export richer Revit schedules
    mapped["material"] = "Unknown"
    mapped["has_window"] = False

    return mapped[
        [
            "room_id",
            "room_name",
            "floor",
            "area_m2",
            "volume_m3",
            "material",
            "has_window",
        ]
    ]