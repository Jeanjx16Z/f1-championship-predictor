import pandas as pd
import numpy as np

F1_POINTS = [25, 18, 15, 12, 10, 8, 6, 4, 2, 1]


# ==========================================================
# TEAM REGULATION RESET LAYER
# ==========================================================

def generate_team_2026(team_baseline: pd.DataFrame, shock_std: float = 0.8):
    team_df = team_baseline.copy()

    team_df["regulation_shock"] = np.random.normal(
        0, shock_std, size=len(team_df)
    )

    team_df["team_2026_rating"] = (
        team_df["team_base_rating"] + team_df["regulation_shock"]
    )

    return team_df[["team", "team_2026_rating"]]


# ==========================================================
# SINGLE RACE SIMULATION
# ==========================================================

def simulate_race(driver_df: pd.DataFrame, noise_std: float = 0.07) -> pd.DataFrame:
    df = driver_df.copy()

    # Fallback logic biar backward compatible
    if "driver_skill" in df.columns:
        skill = df["driver_skill"]
    else:
        skill = df["rating"]

    if "team_2026_rating" in df.columns:
        team_strength = df["team_2026_rating"]
    else:
        team_strength = 0

    # Performance calculation
    df["performance_score"] = (
        skill
        + team_strength
        + np.random.normal(0, noise_std, size=len(df))
    )

    # DNF simulation
    random_vals = np.random.rand(len(df))
    df["dnf_flag"] = random_vals < df["dnf_rate"]

    # Sort by performance
    df = df.sort_values("performance_score", ascending=False).reset_index(drop=True)

    # Assign finish positions
    df["sim_finish_position"] = np.arange(1, len(df) + 1)

    # Push DNFs to bottom
    if df["dnf_flag"].any():
        dnf_drivers = df[df["dnf_flag"]].copy()
        non_dnf = df[~df["dnf_flag"]].copy()

        non_dnf["sim_finish_position"] = np.arange(1, len(non_dnf) + 1)
        dnf_drivers["sim_finish_position"] = np.arange(
            len(non_dnf) + 1, len(df) + 1
        )

        df = pd.concat([non_dnf, dnf_drivers]).reset_index(drop=True)

    # Assign points
    df["sim_points"] = 0
    for i in range(min(len(F1_POINTS), len(df))):
        df.loc[i, "sim_points"] = F1_POINTS[i]

    return df.sort_values("sim_finish_position").reset_index(drop=True)


# ==========================================================
# FULL SEASON SIMULATION
# ==========================================================

def simulate_season(
    driver_df: pd.DataFrame,
    team_baseline: pd.DataFrame = None,
    n_races: int = 24,
    noise_std: float = 0.10,
    shock_std: float = 0.8
) -> pd.DataFrame:

    df = driver_df.copy()

    # Kalau tidak pakai team baseline → pure driver mode
    if team_baseline is None:
        df["combined_rating"] = df["rating"]
    else:
        team_2026 = generate_team_2026(team_baseline, shock_std=shock_std)
        df = df.merge(team_2026, on="team", how="left")
        df["team_2026_rating"] = df["team_2026_rating"].fillna(0)
        df["combined_rating"] = df["rating"] + df["team_2026_rating"]

    df["total_points"] = 0

    for _ in range(n_races):
        race_df = df.copy()
        race_df["rating"] = race_df["combined_rating"]

        race_result = simulate_race(race_df, noise_std=noise_std)
        df["total_points"] += race_result["sim_points"].values

    df = df.sort_values("total_points", ascending=False).reset_index(drop=True)
    df["final_position"] = df.index + 1

    return df[["driver", "total_points", "final_position"]]
# ==========================================================
# MONTE CARLO ENGINE
# ==========================================================

def simulate_many_seasons(
    driver_df: pd.DataFrame,
    team_baseline: pd.DataFrame = None,
    n_sims: int = 100,
    n_races: int = 24,
    noise_std: float = 0.10,
    shock_std: float = 0.8
) -> pd.Series:

    champions = []

    for _ in range(n_sims):
        season = simulate_season(
            driver_df=driver_df,
            team_baseline=team_baseline,
            n_races=n_races,
            noise_std=noise_std,
            shock_std=shock_std
        )

        champion = season.iloc[0]["driver"]
        champions.append(champion)

    return pd.Series(champions).value_counts(normalize=True)