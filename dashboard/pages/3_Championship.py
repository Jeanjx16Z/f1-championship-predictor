import streamlit as st
import matplotlib.pyplot as plt
import fastf1
from utils.standings import (
    calculate_driver_standing,
    calculate_constructor_standing
)
from utils.team_color import TEAM_COLORS
#PAGE TIILE

st.title(" F1 2026 Championship Standings")

YEAR = 2026

#DRIVER CHAMPIONSHIP
st.subheader("Driver Championsip")

with st.spinner("Calculating standings ..."):
    driver_standings = calculate_driver_standing(YEAR)

st.dataframe(driver_standings, width='stretch')

#Driver Points Chart

fig, ax = plt.subplots()

driver_colors = [] 

for driver in driver_standings["Driver"]:
    try:
        team = fastf1.plotting.driver_team(driver)
    except:
        team = "#888888"

    driver_colors.append(team)

ax.barh(
    driver_standings["Driver"],
    driver_standings["Points"],
    color = driver_colors
)

ax.set_xlabel("Points")
ax.set_ylabel("Driver")
ax.invert_yaxis()

st.pyplot(fig)
plt.close(fig)
st.markdown("---")

#Constructor Championship 
st.subheader("Constructor Championship")

with st.spinner("Calculating standings..."):
    constructor_standings = calculate_constructor_standing(YEAR) 

st.dataframe(constructor_standings, width = 'stretch')

# Cosntructor Charts

fig, ax = plt.subplots()

team_colors = [
    TEAM_COLORS.get(team, "#888888")
    for team in constructor_standings["Team"]
]

ax.barh(
    constructor_standings["Team"],
    constructor_standings["Points"],
    color=team_colors
)

ax.set_xlabel("Points")
ax.set_ylabel("Team")
ax.invert_yaxis()

st.pyplot(fig)

plt.close(fig)