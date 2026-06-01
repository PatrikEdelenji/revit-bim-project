import pandas as pd


REQUIRED_COLUMNS = [
    "room_id",
    "room_name",
    "floor",
    "area_m2",
    "volume_m3",
    "material",
    "has_window",
]


def validate_rooms_schema(df: pd.DataFrame) -> None:
    """
    Validate that the rooms dataframe has the expected columns.
    """

    missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")


def clean_rooms(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean room data exported from Revit.
    """

    validate_rooms_schema(df)

    cleaned_df = df.copy()

    cleaned_df["room_id"] = cleaned_df["room_id"].astype(str).str.strip()
    cleaned_df["room_name"] = cleaned_df["room_name"].astype(str).str.strip()
    cleaned_df["material"] = cleaned_df["material"].astype(str).str.strip()

    cleaned_df["floor"] = cleaned_df["floor"].astype(str).str.strip()
    cleaned_df["area_m2"] = pd.to_numeric(cleaned_df["area_m2"], errors="coerce")
    cleaned_df["volume_m3"] = pd.to_numeric(cleaned_df["volume_m3"], errors="coerce")

    cleaned_df["has_window"] = cleaned_df["has_window"].astype(str).str.lower().map(
        {
            "true": True,
            "false": False,
            "yes": True,
            "no": False,
            "1": True,
            "0": False,
        }
    )

    cleaned_df = cleaned_df.dropna(
        subset=["room_id", "room_name", "area_m2", "volume_m3"]
    )

    cleaned_df = cleaned_df[cleaned_df["area_m2"] > 0]
    cleaned_df = cleaned_df[cleaned_df["volume_m3"] > 0]

    return cleaned_df