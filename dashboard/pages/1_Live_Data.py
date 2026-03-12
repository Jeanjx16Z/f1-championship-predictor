import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

from utils.fastf1_loader import load_race_session, load_schedule

# ==============================
# Page Title
# ==============================

st.title("📡 F1 2026 Live Data")

YEAR = 2026

# ==============================
# Load Season Schedule
# ==============================

schedule = load_schedule(YEAR)

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
    session = load_race_session(YEAR, selected_gp)

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

    if pos.empty:
        raise Exception("No position data")

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
    plt.close(fig)

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

st.dataframe(race_table, width='stretch')

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