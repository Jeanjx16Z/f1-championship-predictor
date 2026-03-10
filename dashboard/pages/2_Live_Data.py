import streamlit as st
import fastf1
import pandas as pd
from datetime import datetime
import os 

import os
from pathlib import Path

# locate project root
project_root = Path(__file__).resolve().parents[2]

cache_dir = project_root / "cache"

# create cache folder if it doesn't exist
cache_dir.mkdir(exist_ok=True)

fastf1.Cache.enable_cache(str(cache_dir))

st.title("F1 2026 Live Data")

YEAR = 2026

#load season schedule
schedule = fastf1.get_event_schedule(YEAR)

schedule = schedule[schedule["EventFormat"] != "testing"]

gp_list = schedule["EventName"].tolist()

selected_gp = st.selectbox("Select Grand Prix", gp_list)

st.markdown("---")

try:
    session = fastf1.get_session(
        YEAR,
        selected_gp,
        "R"
    )

    session.load()

    results = session.results
    #Race Result
    st.subheader(f"🏁 Race Results {selected_gp}")

    race_table = results[
        ["Position", "Abbreviation", "TeamName", "Time","Points"]

    ]

    race_table.columns = [
        "Position",
        "Driver",
        "Team",
        "Finish Time",
        "Points"
    ]

    st.dataframe(race_table)
    st.markdown("---")

    #Driver Championship Standings
    st.subheader("🏆 2026 Driver Standings")

    driver_points = results[
        ["Driver", "Abbreviation", "Points"]
    ]
    driver_points.columns = [
        "Driver",
        "Abbreviation",
        "Points"
    ]
    driver_points = driver_points.sort_values(
        "Points",
        ascending=False
    )

    st.dataframe(driver_points)
    st.markdown("---")

    #Constructor Championship
    st.subheader("🚘 Constructor Standings")

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

except Exception:
    st.info(
        f"""
        Data for ++ {selected_gp}++ is not yet available.
        This race may bot have taken place yet
        """
    )
