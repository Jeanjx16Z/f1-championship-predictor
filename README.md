# 🏎️ F1 Championship Predictor & Analytics Dashboard

A data-driven Formula 1 championship prediction and race analytics platform combining Monte Carlo simulation, FastF1 telemetry data, and interactive Streamlit dashboards.

This project integrates **season simulation**, **live race analytics**, and **championship standings calculation** into a unified Formula 1 analytics toolkit.

---

# 📌 Project Objectives

* Build a Monte Carlo-based championship prediction model
* Combine driver skill and team performance
* Simulate full F1 seasons probabilistically
* Calculate championship probabilities
* Provide real-time race analytics dashboard
* Visualize telemetry and performance comparisons
* Compute FIA-compliant championship standings (Race + Sprint + Fastest Lap)

---

# 📂 Project Structure

```
f1-championship-predictor/
│
├── dashboard/
│   ├── pages/
│   │   ├── 1_Live_Data.py
│   │   ├── 3_Championship.py
│   │   └── Races_Analytic.py
│   │
│   └── utils/
│       ├── fastf1_loader.py
│       ├── standings.py
│       └── plotting.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── src/
│   ├── simulator.py
│   └── rating_engine.py
│
└── README.md
```

---

# 📊 Dashboard Features

## 📡 Live Data Page

* Session selector (Practice / Qualifying / Sprint / Race)
* Automatic session detection from FastF1
* Circuit layout visualization (2025 fallback for 2026)
* Session results table
* Fast loading via Streamlit caching

---

## 🏆 Championship Page

Custom championship calculation including:

* Race points
* Sprint points
* Fastest lap bonus (+1 point, top 10 only)

This improves accuracy compared to official standings that may not immediately include fastest lap adjustments.

---

## 📈 Race Analytics Page

Interactive visualization tools:

### Lap Time Comparison

Compare race pace between multiple drivers.

### Speed Telemetry

Speed vs distance comparison using fastest lap telemetry.

### Position Changes

Race position evolution across laps.

---

# 🧠 Championship Scoring Engine

The standings engine computes:

```
Total Points =
Race Points
+ Sprint Points
+ Fastest Lap Bonus
```

Rules implemented:

* Official FIA race points (Top 10)
* Sprint race points (Top 8)
* Fastest lap bonus only if driver finishes Top 10

---

# 🎲 Monte Carlo Championship Simulation

The simulator models season outcomes using:

```
performance_score =
driver_skill
+ team_strength
+ random_noise
```

Supports:

* Driver-only simulation
* Driver + team baseline
* Regulation reset scenarios

---

# 🔧 Regulation Reset Simulation (2026)

Team performance shock applied:

```
team_2026_rating =
team_base_rating + random_shock
```

Models:

* Regulation changes
* Competitive reshuffling
* Aero reset scenarios

---

# 📊 Race Analytics Visualization Engine

Reusable plotting functions:

* `plot_lap_times()`
* `plot_speed_trace()`
* `plot_position_changes()`

Designed for modular reuse across dashboard pages.

---

# ⚙️ Model Parameters

| Parameter   | Description             |
| ----------- | ----------------------- |
| `noise_std` | Race variability        |
| `shock_std` | Regulation reset impact |
| `n_races`   | Number of races         |
| `n_sims`    | Monte Carlo simulations |

---

# 🚀 Current Capabilities

The platform now supports:

* Live race data visualization
* Telemetry-based analytics
* Custom championship standings
* Sprint + fastest lap integration
* Monte Carlo championship prediction
* Modular plotting engine
* Streamlit interactive dashboard

---

# 🛠️ Technologies Used

* Python
* Pandas
* NumPy
* Streamlit
* FastF1
* Matplotlib
* Monte Carlo Simulation

---

# 📈 Project Status

Current version includes:

* Stable simulation engine
* Fully working analytics dashboard
* FIA-compliant standings calculation
* Telemetry visualization tools

Next planned improvements:

* Championship progression charts
* Prediction visualization dashboard
* Track-specific performance modeling
* Constructor championship simulation
* AI-based race insights

---

# 📜 License

This project is for educational and analytical purposes only.
Formula 1 data belongs to respective rights holders.
