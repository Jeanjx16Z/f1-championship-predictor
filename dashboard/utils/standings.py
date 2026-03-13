import pandas as pd
import streamlit as st
from datetime import datetime
from utils.fastf1_loader import load_race_session, load_schedule
@st.cache_data
def calculate_driver_standing(year: int):
    
    schedule = load_schedule(year)

    driver_points = {}

    today = datetime.today()

    completed_races = schedule[schedule["EventDate"] < today]

    for _, event in completed_races.iterrows():
        gp_name = event["EventName"]

        try:
            session = load_race_session(year, gp_name)
            results = session.results

        except Exception:
            continue
        
        for _, row in results.iterrows():
            driver = row["Abbreviation"]

            points = pd.to_numeric(
                row["Points"],
                errors="coerce"
            )

            if pd.isna(points):
                points = 0

            if driver not in driver_points:
                driver_points[driver] = 0
            
            driver_points[driver] += points

    standings = pd.DataFrame(
        driver_points.items(),
        columns=["Driver", "Points"]
    )

    standings = standings.sort_values(
        "Points",
        ascending=False
    ).reset_index(drop=True)

    standings["Position"] = standings.index + 1

    return standings

@st.cache_data
def calculate_constructor_standing(year: int):
    schedule = load_schedule(year)

    team_points = {}

    today = datetime.today()

    completed_races = schedule[schedule["EventDate"] < today]

    for _, event in completed_races.iterrows():
        gp_name = event["EventName"]

        try:
            session = load_race_session(year, gp_name)
            results = session.results

        except Exception:
            continue

        for _, row in results.iterrows():
            team = row["TeamName"]
            points = row["Points"]

            if team not in team_points:
                team_points[team] = 0

            team_points[team] += points

    standings = pd.DataFrame(
        team_points.items(),
        columns=["Team", "Points"]
    )

    standings = standings.sort_values(
        "Points",
        ascending=False
    ).reset_index(drop=True)

    standings["Position"] = standings.index + 1

    return standings