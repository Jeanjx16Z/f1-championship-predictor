import streamlit as st
import fastf1
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# ==============================
# FastF1 Cache Setup
# ==============================

project_root = Path(__file__).resolve().parents[2]
cache_dir = project_root / "cache"
cache_dir.mkdir(exist_ok=True)

fastf1.Cache.enable_cache(str(cache_dir))

# ==============================
# Page Title
# ==============================

st.title("📡 F1 2026 Live Data")

YEAR = 2026

# ==============================
# Load Season Schedule
# ==============================

schedule = fastf1.get_event_schedule(YEAR)
schedule = schedule[schedule["EventFormat"] != "testing"]

gp_list = schedule["EventName"].tolist()

selected_gp = st.selectbox(
    "Select Grand Prix",
    gp_list
)

st.markdown("---")

# ==============================
# Load Race Session
# ==============================

try:
    session = fastf1.get_session(YEAR, selected_gp, "R")
    session.load()

except Exception:
    st.warning(
        f"Race data for **{selected_gp}** is not available yet."
    )
    st.stop()

# ==============================
# Circuit Layout
# ==============================

st.subheader(f"🗺 Circuit Layout — {selected_gp}")

try:

    lap = session.laps.pick_fastest()

    if lap is None:
        raise Exception("No lap data")

    pos = lap.get_pos_data()

    track = pos.loc[:, ["X", "Y"]].to_numpy()

    # Try to get circuit info
    try:
        circuit_info = session.get_circuit_info()
        track_angle = circuit_info.rotation / 180 * np.pi
    except:
        circuit_info = None
        track_angle = 0

    def rotate(xy, angle):
        rot_mat = np.array([
            [np.cos(angle), np.sin(angle)],
            [-np.sin(angle), np.cos(angle)]
        ])
        return np.matmul(xy, rot_mat)

    rotated_track = rotate(track, track_angle)

    fig, ax = plt.subplots()

    ax.plot(
        rotated_track[:, 0],
        rotated_track[:, 1],
        linewidth=3
    )

    # Plot corners only if available
    if circuit_info is not None and circuit_info.corners is not None:

        for _, corner in circuit_info.corners.iterrows():

            txt = f"{corner['Number']}{corner['Letter']}"

            corner_xy = rotate(
                np.array([corner["X"], corner["Y"]]),
                track_angle
            )

            ax.scatter(
                corner_xy[0],
                corner_xy[1],
                s=80
            )

            ax.text(
                corner_xy[0],
                corner_xy[1],
                txt,
                ha="center",
                va="center"
            )

    ax.set_aspect("equal")
    ax.axis("off")

    st.pyplot(fig)

except Exception as e:

    st.warning("Telemetry data for circuit layout is not available yet.")

# ==============================
# Race Result
# ==============================

st.subheader(f"🏁 Race Results — {selected_gp}")

results = session.results

race_table = results[
    ["Position", "Abbreviation", "TeamName", "Points"]
].copy()

race_table.columns = [
    "Position",
    "Driver",
    "Team",
    "Points"
]

st.dataframe(race_table)

st.markdown("---")

# ==============================
# Driver Standings
# ==============================

st.subheader("🏆 2026 Driver Standings")

driver_points = results[
    ["Abbreviation", "Points"]
].copy()

driver_points.columns = [
    "Driver",
    "Points"
]

driver_points = driver_points.sort_values(
    "Points",
    ascending=False
)

st.dataframe(driver_points)

st.markdown("---")

# ==============================
# Constructor Standings
# ==============================

st.subheader("🏭 Constructor Standings")

team_points = results.groupby("TeamName")[
    "Points"
].sum().reset_index()

team_points.columns = [
    "Team",
    "Points"
]

team_points = team_points.sort_values(
    "Points",
    ascending=False
)

st.dataframe(team_points)