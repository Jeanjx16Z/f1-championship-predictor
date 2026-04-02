import streamlit as st
import fastf1 
import pandas as pd
from utils.fastf1_loader import load_race_session, load_schedule
from utils.plotting import (
    plot_lap_times,
    plot_speed_trace,
    plot_position_changes,
    plot_tire_strategy,
)

st.title("📊 Race Analysis")

YEAR = 2026

# Load Schedule

schedule = load_schedule(YEAR)

gp_list = schedule["EventName"].tolist()

selected_gp = st.selectbox(
    "Select Grand Prix",
    gp_list
)

# Load Race Session

try:
    session = load_race_session(
        YEAR,
        selected_gp,
        "Race"
    )
    session.load()   

except Exception:
    st.warning("Race data not available")
    st.stop()

laps = session.laps

# Driver Selection

drivers =  laps["Driver"].unique().tolist()

selected_driver = st.multiselect(
    "Select Driver (Lap Comparison)",
    drivers,
    default=drivers[:2]
)

# 1.Lap Time Comparison

st.subheader("📈 Lap Time Comparison")

if selected_driver:
    fig = plot_lap_times(laps, selected_driver)
    st.pyplot(fig) 

# 2.Speed Telemetry

st.subheader("🚀 Speed Telemetry")

selected_driver = st.selectbox(
    "Select Driver (Telemetry)",
    drivers
)
try: 

    lap = laps.pick_driver(selected_driver).pick_fastest()

    fig = plot_speed_trace(lap, selected_driver)
    st.pyplot(fig)

except Exception:
    st.warning("No Telemetry Data Available.")

# 3.Position Changes

st.subheader("🏁 Position Changes")
fig = plot_position_changes(laps)
st.pyplot(fig) 


# 3.Tire Strategy
st.subheader("🛞 Tire Strategy")

fig = plot_tire_strategy(laps)
st.pyplot(fig)