import streamlit as st
import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from src.simulator import simulate_many_seasons

#PAGE TIILE
st.markdown("## 🏆 Championship Simulation")
st.markdown("Monte Carlo Simulation of the 2026 F1 season based on curent model input")
st.markdown("___")

#LOAD DATA
@st.cache_data
def load_model_input():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    file_path = os.path.join(root_dir, "data", "processed", "model_input_2025.csv")
    return pd.read_csv(file_path)

model_input = load_model_input()

simulation_result = simulate_many_seasons(
    model_input,
    n_sims=5000
)

champion_prob = simulation_result.sort_values(
    "champion_prob",
    ascending=False
)

st.bar_chart(
    champion_prob.set_index("driver")["champion_prob"]
)
#DISPLAY RESULT 
st.subheader("Championship Probability")

st.dataframe(
    champion_prob[
        ["driver", "champion_prob", "p2_prob", "p3_prob"]
    ]
)