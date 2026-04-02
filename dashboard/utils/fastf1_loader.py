import fastf1
import streamlit as st
from pathlib import Path

#Setup cache directory automatically
project_root = Path(__file__).resolve().parents[2]
cache_dir = project_root / "cache"
cache_dir.mkdir(exist_ok=True)

fastf1.Cache.enable_cache(str(cache_dir))
@st.cache_data
def load_race_session(year, gp, session_type="Race"):
    session = fastf1.get_session(year, gp, session_type)
    session.load(
        telemetry=True,
        weather=False,
        messages=False
    )

    return session
@st.cache_data
def load_schedule(year):
    schedule =  fastf1.get_event_schedule(year)
    schedule = schedule[schedule["EventFormat"] != "testing"]

    return schedule