# 🏎️ F1 Championship Predictor – 2025 Season Simulation

A Monte Carlo-based Formula 1 championship prediction model built using historical driver performance metrics and team performance baselines.

This project simulates a full F1 season (24 races) and estimates each driver's probability of becoming World Champion under different competitive scenarios.

---

# 📌 Project Objective

The goal of this project is to:

- Build a data-driven F1 championship prediction model
- Combine driver skill and team performance
- Simulate season outcomes using probabilistic modeling
- Estimate championship probability using Monte Carlo simulation
- Model competitive regulation reset scenarios (e.g., 2026 regulation changes)

---

# 📂 Project Structure
```
f1-championship-predictor/
│
├── data/
│ ├── raw/
│ └── processed/
│ ├── driver_ratings_2025.csv
│ └── team_baseline_2025.csv
│
├── notebooks/
│ └── 01_data_exploration.ipynb
│
├── src/
│ ├── simulator.py
│ └── rating_engine.py
│
└── README.md
```


---

# 🔎 Phase 1 – Driver Rating Model

We engineered a driver rating system based on:

- Average points
- Average finish position
- Standard deviation of finish
- DNF rate
- Wins
- Podiums
- Consistency score

Each feature was normalized and combined into a final:

This rating represents the intrinsic performance strength of each driver.

Output: driver_ratings_2025.csv 


---

# 🏁 Phase 2 – Race Simulation Engine

We built a probabilistic race simulator:

### Core Logic

For each race:
```
performance_score = driver_skill + team_strength + random_noise 
```

Where:

- `driver_skill` → derived from rating
- `team_strength` → team baseline performance
- `random_noise` → stochastic race variation
- DNF probability → applied per driver
```
Race results are sorted by performance score and assigned official F1 points:
[25, 18, 15, 12, 10, 8, 6, 4, 2, 1]
```
---

# 🏆 Phase 3 – Season Simulation

A full season is simulated across:


For each season:

- All races are simulated
- Points are accumulated
- Final standings are computed
- Champion is determined

```
Function used: simulate_season()
```
---

# 🎲 Phase 4 – Monte Carlo Championship Probability

We simulate many seasons:
```
n_sims = 100–500+
```


Each simulation:

1. Runs a full 24-race season
2. Determines the champion
3. Stores the result

Final output:
```
champion_probability
Example output:
VER 0.42
NOR 0.27
PIA 0.18
RUS 0.09
LEC 0.04
```


---

# 🔧 Phase 5 – Team Baseline Integration

To increase realism, we introduced:
team_base_rating
Each driver's performance became:
```
combined_rating = driver_rating + team_rating
```

This allowed modeling:

- Team dominance eras
- Constructor performance shifts
- Competitive reshuffling

Output dataset:
team_baseline_2025.csv


---

# 🚨 Phase 6 – Regulation Reset Simulation (2026 Scenario)

We implemented a regulation shock system:

At the start of each simulated season:
```
team_2026_rating = team_base_rating + random_shock
```

These models:

- Major regulation changes
- Aero resets
- Competitive grid reshuffling

Parameter: shock_std


Higher values → more chaotic grid  
Lower values → stable dominance

---

# ⚙️ Current Simulation Modes

The simulator now supports:

### 1️⃣ Driver-Only Mode
Pure driver skill simulation.

### 2️⃣ Driver + Team Mode
Driver skill combined with team baseline.

### 3️⃣ Regulation Reset Mode
Driver + team + stochastic team shock.

---

# 📊 Model Parameters

| Parameter | Description |
|-----------|-------------|
| `noise_std` | Race-to-race variability |
| `shock_std` | Regulation-era team reshuffle intensity |
| `n_races` | Number of races per season |
| `n_sims` | Number of Monte Carlo simulations |

---

# 🧠 Key Insights So Far

- Small noise → deterministic champion
- Large shock_std → realistic title fights
- Rating gaps strongly influence probability distribution
- DNF rates meaningfully impact championship variance

---

# 🚀 Next Planned Improvements

- Race-by-race simulation using `round_number`
- Track-specific performance modifiers
- Constructor championship simulation
- Bayesian rating updates mid-season
- Visualization dashboard

---

# 🛠️ Technologies Used

- Python
- Pandas
- NumPy
- Monte Carlo Simulation
- Probabilistic Modeling

---

# 📈 Current Status

The simulation engine is functional and structurally stable.

The model successfully:

- Generates realistic season standings
- Estimates championship probability
- Supports regulation-era simulations

Further calibration is ongoing to balance dominance vs. competitive variance.

---

# 📜 License

This project is for educational and analytical purposes only.
Formula 1 data belongs to respective rights holders.
