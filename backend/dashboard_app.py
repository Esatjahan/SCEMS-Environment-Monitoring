"""
dashboard_app.py

Simple Streamlit dashboard for SCEMS.
Shows real-time-ish synthetic data + alerts + basic analytics.
"""

import time
import pandas as pd
import streamlit as st

from sensors_simulation import generate_random_frame, frame_to_dict
from threshold_engine import evaluate_all


st.set_page_config(
    page_title="SCEMS Dashboard",
    layout="wide",
)

st.title("SCEMS - Smart Community Environment Monitoring System")
st.subheader("Simulation-based Community Environment Monitoring (Gazipur)")

# Sidebar controls
st.sidebar.header("Simulation Controls")
num_frames = st.sidebar.slider("Number of frames to simulate", 10, 200, 50, step=10)
delay_ms = st.sidebar.slider("Delay per frame (ms)", 0, 1000, 200, step=50)
auto_run = st.sidebar.button("Run Simulation")


# Session state for data
if "data" not in st.session_state:
    st.session_state["data"] = pd.DataFrame()


def run_simulation():
    frames = []
    for _ in range(num_frames):
        frame = generate_random_frame()
        eval_result = evaluate_all(frame)
        merged = frame_to_dict(frame, eval_result)
        frames.append(merged)
        if delay_ms > 0:
            time.sleep(delay_ms / 1000.0)
    df_new = pd.DataFrame(frames)
    if st.session_state["data"].empty:
        st.session_state["data"] = df_new
    else:
        st.session_state["data"] = pd.concat(
            [st.session_state["data"], df_new], ignore_index=True
        )


if auto_run:
    run_simulation()

df = st.session_state["data"]

st.markdown("### Real-time Data Table")
st.dataframe(df.tail(20), use_container_width=True)

if not df.empty:
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Temperature vs Time")
        st.line_chart(df["temperature"])

        st.markdown("#### Soil Moisture vs Time")
        st.line_chart(df["soil_moisture"])

    with col2:
        st.markdown("#### AQI vs Time")
        st.line_chart(df["aqi"])

        st.markdown("#### Crowd Estimate vs Time")
        st.line_chart(df["crowd_estimate"])

    st.markdown("#### Alert Priority Distribution")
    priority_counts = df["global_priority"].value_counts()
    st.bar_chart(priority_counts)

    st.markdown("#### Latest Alert Snapshot")
    last_row = df.iloc[-1].to_dict()
    st.json(
        {
            "soil_status": last_row.get("soil_status"),
            "heat_status": last_row.get("heat_status"),
            "aqi_status": last_row.get("aqi_status"),
            "crowd_status": last_row.get("crowd_status"),
            "security_status": last_row.get("security_status"),
            "light_status": last_row.get("light_status"),
            "global_priority": last_row.get("global_priority"),
        }
    )
else:
    st.info("Click 'Run Simulation' in the sidebar to generate data.")
