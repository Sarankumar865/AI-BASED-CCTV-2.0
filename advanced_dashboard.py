import sqlite3
from pathlib import Path
from datetime import date, timedelta

import pandas as pd
import streamlit as st

# Database path
DB_PATH = Path(__file__).resolve().parent / "cctv_events.db"

# Page settings
st.set_page_config(
    page_title="AI CCTV 2.0",
    page_icon="📹",
    layout="wide"
)

# Dashboard title
st.title("AI CCTV 2.0")
st.subheader("Intelligent Surveillance Dashboard")
st.caption(
    "AI detection • Restricted-zone monitoring • Event analytics"
)

# Refresh button
if st.button("Refresh Dashboard"):
    st.rerun()

# Read database
try:
    with sqlite3.connect(DB_PATH, timeout=5) as con:

        # Read event history
        events = pd.read_sql_query(
            """
            SELECT id, event_time, event_type, description
            FROM events
            ORDER BY event_time DESC, id DESC
            """,
            con
        )

        # Read latest camera status
        status = pd.read_sql_query(
            """
            SELECT updated_at, people_count, zone_occupied
            FROM camera_status
            WHERE id = 1
            """,
            con
        )

except (sqlite3.Error, pd.errors.DatabaseError) as error:
    st.error(f"Database error: {error}")
    st.info(
        "Check that stage6_cctv_database.py has created "
        "the required tables in cctv_events.db."
    )
    st.stop()

# Camera status
st.header("Camera Status")

if not status.empty:
    latest = status.iloc[0]

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "People Detected",
        int(latest["people_count"])
    )

    zone = (
        "Occupied"
        if int(latest["zone_occupied"]) == 1
        else "Clear"
    )

    col2.metric("Restricted Zone", zone)
    col3.metric("Last Update", str(latest["updated_at"]))

else:
    st.warning(
        "No camera status available. "
        "Start stage6_cctv_database.py first."
    )

st.divider()

# Security analytics
st.header("Security Analytics")

today = date.today()
today_text = today.isoformat()

if not events.empty:
    event_dates = events["event_time"].astype(str).str[:10]

    today_count = int(
        (event_dates == today_text).sum()
    )

    alert_count = int(
        (events["event_type"] == "RESTRICTED_ZONE").sum()
    )
else:
    today_count = 0
    alert_count = 0

col1, col2, col3 = st.columns(3)

col1.metric("Events Today", today_count)
col2.metric("Total Events", len(events))
col3.metric("Total Zone Alerts", alert_count)

st.divider()

# Event history and filters
st.header("Event History")

col1, col2, col3 = st.columns(3)

with col1:
    start_date = st.date_input(
        "Start date",
        value=today - timedelta(days=7)
    )

with col2:
    end_date = st.date_input(
        "End date",
        value=today
    )

with col3:
    available_types = (
        events["event_type"].dropna().unique().tolist()
        if not events.empty
        else []
    )

    types = ["All"] + sorted(available_types)

    event_type = st.selectbox(
        "Event type",
        types
    )

# Filter events by date and event type
if start_date > end_date:
    st.error("Start date cannot be after end date.")
    filtered = events.iloc[0:0].copy()

else:
    event_dates = pd.to_datetime(
        events["event_time"],
        errors="coerce"
    ).dt.date

    filtered = events[
        event_dates.notna()
        & (event_dates >= start_date)
        & (event_dates <= end_date)
    ].copy()

    if event_type != "All":
        filtered = filtered[
            filtered["event_type"] == event_type
        ]

# Search event descriptions
search_text = st.text_input(
    "Search event descriptions",
    placeholder="Example: person detected"
)

if search_text:
    filtered = filtered[
        filtered["description"].str.contains(
            search_text,
            case=False,
            na=False
        )
    ]

st.write(f"Matching records: {len(filtered)}")

if filtered.empty:
    st.info("No matching events found.")

else:
    st.dataframe(
        filtered,
        width="stretch",
        hide_index=True
    )

    # CSV download
    csv_data = filtered.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="Download Events as CSV",
        data=csv_data,
        file_name="ai_cctv_events.csv",
        mime="text/csv"
    )

# Daily event trend chart
st.divider()
st.header("Daily Event Trend")

if not events.empty:
    chart_data = events.copy()

    chart_data["Date"] = pd.to_datetime(
        chart_data["event_time"],
        errors="coerce"
    ).dt.date

    daily = (
        chart_data.dropna(subset=["Date"])
        .groupby("Date")
        .size()
        .reset_index(name="Events")
        .sort_values("Date")
    )

    if not daily.empty:
        daily_chart = daily.set_index("Date")["Events"]
        st.bar_chart(daily_chart)
    else:
        st.info("No dated events available for the chart.")

else:
    st.info(
        "The chart will appear when events are recorded."
    )

# Footer
st.caption(
    "AI CCTV 2.0 | Event analytics and database monitoring"
)