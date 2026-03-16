import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import fastf1

from utils.fastf1_loader import load_race_session, load_schedule

# ==============================
# Page Title
# ==============================

st.title("📡 F1 2026 Live Data")

YEAR = 2026
LAYOUT_YEAR = 2025


# ==============================
# Cache Functions
# ==============================

@st.cache_data(show_spinner=False)
def get_session(year, gp, session_code):

    session = load_race_session(year, gp, session_code)
    session.load()

    return session


@st.cache_data(show_spinner=False)
def get_layout_session(gp):

    session = load_race_session(
        LAYOUT_YEAR,
        gp,
        "Race"
    )

    session.load()

    return session


@st.cache_data(show_spinner=False)
def get_event_sessions(year, gp):

    event = fastf1.get_event(year, gp)

    sessions=[]

    for i in range(1, 6):

        session_name = event.get(f"Session{i}")

        if session_name is not None:
            sessions.append(session_name)

    return sessions

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
# Auto Detect Sessions
# ==============================

available_sessions = get_event_sessions(
    YEAR,
    selected_gp
)

selected_session = st.selectbox(
    "Select Session",
    available_sessions
)

SESSION_MAP = {
    "Practice 1": "FP1",
    "Practice 2": "FP2",
    "Practice 3": "FP3",
    "Sprint Qualifying": "Sprint Qualifying",
    "Sprint": "Sprint",
    "Qualifying": "Qualifying",
    "Race": "Race"
}
session_code = SESSION_MAP[selected_session]
# ==============================
# Load Session
# ==============================

try:

    session = get_session(
        YEAR,
        selected_gp,
        session_code
    )

except Exception:

    st.warning(
        f"{selected_session} data for **{selected_gp}** is not available yet."
    )

    st.stop()


# ==============================
# Circuit Layout
# ==============================

st.subheader(f"🗺 Circuit Layout — {selected_gp}")

try:

    layout_session = get_layout_session(selected_gp)

    lap = layout_session.laps.pick_fastest()

    if lap is None:
        raise Exception("No lap data")

    pos = lap.get_pos_data()

    if pos.empty:
        raise Exception("No position data")

    track = pos.loc[:, ["X", "Y"]].to_numpy()

    try:

        circuit_info = layout_session.get_circuit_info()

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

except Exception:

    st.warning(
        "Telemetry data for circuit layout is not available."
    )


# ==============================
# Session Results
# ==============================

st.subheader(f"🏁 {selected_session} Results — {selected_gp}")

results = session.results

display_columns = []

if "Position" in results.columns:
    display_columns.append("Position")

if "Abbreviation" in results.columns:
    display_columns.append("Abbreviation")

if "TeamName" in results.columns:
    display_columns.append("TeamName")

if "Time" in results.columns:
    display_columns.append("Time")

if "Points" in results.columns:
    display_columns.append("Points")

race_table = results[display_columns].copy()

rename_map = {
    "Abbreviation": "Driver",
    "TeamName": "Team"
}

race_table = race_table.rename(columns=rename_map)

st.dataframe(
    race_table,
    width="stretch"
)

st.markdown("---")