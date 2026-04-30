import streamlit as st
from src.ai.anomaly_detection import detect_room_anomalies
from src.storage.load_processed import load_rooms_parquet

from src.analytics.room_metrics import (
    get_total_area_by_floor,
    get_material_summary,
    get_largest_rooms,
)


PARQUET_PATH = "data/processed/rooms.parquet"


st.set_page_config(
    page_title="Revit BIM Analytics Dashboard",
    layout="wide",
)

st.title("Revit BIM Analytics Dashboard")
st.caption("Analytics from Revit-style room data")

area_by_floor = get_total_area_by_floor(PARQUET_PATH)
material_summary = get_material_summary(PARQUET_PATH)
largest_rooms = get_largest_rooms(PARQUET_PATH, limit=5)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total floors", area_by_floor["floor"].nunique())

with col2:
    st.metric("Total rooms", int(area_by_floor["room_count"].sum()))

with col3:
    st.metric("Total area m²", round(area_by_floor["total_area_m2"].sum(), 2))

st.divider()

st.subheader("Total area by floor")
st.bar_chart(area_by_floor, x="floor", y="total_area_m2")

st.subheader("Material summary")
st.dataframe(material_summary, use_container_width=True)

st.subheader("Largest rooms")
st.dataframe(largest_rooms, use_container_width=True)

st.subheader("Anomaly detection")

full_df = load_rooms_parquet(PARQUET_PATH)

anomalies = detect_room_anomalies(full_df)

st.write(f"Detected {len(anomalies)} suspicious rooms")
st.dataframe(anomalies, use_container_width=True)