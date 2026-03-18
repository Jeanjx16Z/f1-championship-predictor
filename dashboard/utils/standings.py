import pandas as pd
import streamlit as st
from datetime import datetime

from utils.fastf1_loader import load_race_session, load_schedule

# Driver Standings

@st.cache_data
def calculate_driver_standings(year: int):
    schedule = load_schedule(year)

    driver_points = {}

    today = datetime.today()

    completed_races = schedule[schedule["EventDate"] <  today]

    for _, event in completed_races.iterrows():
        gp_name = event["EventName"]
        #Race 
        try:
            race = load_race_session(year, gp_name, "Race")
            race.load()

            results = race.results

            for _, row in results.iterrows():
                driver = row["Abbreviation"]

                points = pd.to_numeric(row["Points"], errors="coerce")
                if pd.isna(points):
                    points = 0

                driver_points[driver] = driver_points.get(driver, 0) + points

            #Fastest Lap
            try:
                fastest = race.laps.pick_fastest()

                if fastest is not None:
                    driver = fastest["Driver"]

                    pos = results[
                        results["Abbreviation"] == driver
                    ]["Position"].values

                    if len(pos) > 0 and pos[0] <= 10:
                        driver_points[driver] += 1

            except:
                pass

        except Exception:
            continue

        #SPRINT
        try:
            sprint = load_race_session(year, gp_name, "Sprint")
            sprint.load()


            sprint_results = sprint.results

            for _, row in sprint_results.iterrows():
                driver = row["Abbreviation"]

                points = pd.to_numeric(row["Points"], errors="coerce")
                if pd.isna(points):
                    points = 0 

                driver_points[driver] = driver_points.get(driver, 0) + points

        except:
            pass

    #Convert to DataDrame
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

#Constructor Standings

@st.cache_data
def calculate_constructor_standing(year: int):

    schedule = load_schedule(year)

    team_points = {}

    today = datetime.today()
    completed_races = schedule[schedule["EventDate"] < today]

    for _, event in completed_races.iterrows():
        gp_name = event["EventName"]
        #Race
        try:
            race = load_race_session(year, gp_name, "Race")
            race.load()

            results =  race.results

            for _, row in results.iterrows():
                team = row["TeamName"]

                points = pd.to_numeric(row["Points"], errors = "coerce")
                if pd.isna(points):
                    points = 0

                team_points[team] = team_points.get(team, 0) + points 

        except:
            continue

        # Sprint

        try:
            sprint = load_race_session(year, gp_name, "Sprint")
            sprint.load()

            sprint_results = sprint.results

            for _, row in sprint_results.iterrows():
                team = row["TeamName"]

                points =pd.to_numeric(row["Points"], errors="coerce")
                if pd.isna(points):
                    points = 0

                team_points[team] = team_points.get(team, 0) + points

        except:
            pass
    
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