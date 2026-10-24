import sqlite3
from pathlib import Path
from datetime import date, timedelta

import pandas as pd
import streamlit as st

# Use the database in this project's folder
DB_PATH = Path(__file__).resolve().parent / "cctv_events.db"

st.set_page_config(
    page_title="AI CCTV 2.0",
    page_icon="📹",
    layout="wide"
)

st.title("AI CCTV 2.0 - Security Dashboard")
st.caption("Live camera status and security event history")

# Refresh the dashboard manually
if st.button("Refresh Dashboard"):
    st.rerun()

# Read the latest camera status and event history
with sqlite3.connect(DB_PATH, timeout=5) as connection:
    status = pd.read_sql_query(
        "SELECT * FROM camera_status WHERE id = 1",
        connection
    )

    event_types = pd.read_sql_query(
        "SELECT DISTINCT event_type FROM events ORDER BY event_type",
        connection
    )["event_type"].dropna().tolist()

    events = pd.read_sql_query(
        "SELECT id, event_time, event_type, description "
        "FROM events ORDER BY event_time DESC, id DESC",
        connection
    )

# Latest camera status
st.subheader("Camera Status")

if not status.empty:
    latest = status.iloc[0]

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "People Detected",
        int(latest["people_count"])
    )

    zone_text = (
        "ALERT"
        if int(latest["zone_occupied"]) == 1
        else "Clear"
    )

    col2.metric("Restricted Zone", zone_text)
    col3.metric("Last Camera Update", str(latest["updated_at"]))

else:
    st.warning(
        "No camera status yet. Start stage6_cctv_database.py "
        "and wait for the first update."
    )

st.divider()
st.subheader("Security Event History")

# Filters
col1, col2, col3 = st.columns(3)

with col1:
    start_date = st.date_input(
        "Start date",
        value=date.today() - timedelta(days=7)
    )

with col2:
    end_date = st.date_input(
        "End date",
        value=date.today()
    )

with col3:
    selected_type = st.selectbox(
        "Event type",
        ["All"] + event_types
    )

if start_date > end_date:
    st.error("Start date must be before or equal to end date.")
    filtered = events.iloc[0:0].copy()

else:
    # Compare dates using the YYYY-MM-DD timestamp prefix
    filtered = events[
        (events["event_time"] >= str(start_date))
        & (
            events["event_time"]
            < str(end_date + timedelta(days=1))
        )
    ].copy()

    if selected_type != "All":
        filtered = filtered[
            filtered["event_type"] == selected_type
        ]

# Summary metrics
col1, col2 = st.columns(2)

col1.metric("Matching Events", len(filtered))

zone_events = (
    filtered["event_type"] == "RESTRICTED_ZONE"
).sum()

col2.metric("Restricted-Zone Alerts", int(zone_events))

# Display filtered records
if filtered.empty:
    st.info("No events match the selected filters.")
else:
    st.dataframe(
        filtered,
        use_container_width=True,
        hide_index=True
    )

    csv_data = filtered.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Download Filtered Events (CSV)",
        data=csv_data,
        file_name="cctv_events.csv",
        mime="text/csv"
    )

st.caption(
    "The dashboard reads saved events. It does not record video "
    "or identify individuals."
)