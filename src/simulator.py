import pandas as pd
import numpy as np

F1_POINTS = [25, 18, 15, 12, 10, 8, 6, 4, 2, 1]


# ==========================================================
# SINGLE RACE SIMULATION
# ==========================================================

def simulate_race(model_df: pd.DataFrame, noise_std: float = 0.15) -> pd.DataFrame:
    """
    Simulate one F1 race using combined_base_rating.
    model_df must contain:
        - driver
        - combined_base_rating
        - dnf_rate
    """

    df = model_df.copy()

    # Performance = base strength + race randomness
    df["performance_score"] = (
        df["combined_base_rating"]
        + np.random.normal(0, noise_std, size=len(df))
    )

    # DNF simulation
    df["dnf_flag"] = np.random.rand(len(df)) < df["dnf_rate"]

    # Sort by performance
    df = df.sort_values("performance_score", ascending=False).reset_index(drop=True)

    # Assign provisional positions
    df["sim_finish_position"] = np.arange(1, len(df) + 1)

    # Push DNFs to bottom
    if df["dnf_flag"].any():
        dnf = df[df["dnf_flag"]].copy()
        non_dnf = df[~df["dnf_flag"]].copy()

        non_dnf["sim_finish_position"] = np.arange(1, len(non_dnf) + 1)
        dnf["sim_finish_position"] = np.arange(len(non_dnf) + 1, len(df) + 1)

        df = pd.concat([non_dnf, dnf]).reset_index(drop=True)

    # Assign points
    df["sim_points"] = 0
    for i in range(min(len(F1_POINTS), len(df))):
        df.loc[i, "sim_points"] = F1_POINTS[i]

    return df.sort_values("sim_finish_position").reset_index(drop=True)


# ==========================================================
# FULL SEASON SIMULATION
# ==========================================================

def simulate_season(
    model_df: pd.DataFrame,
    n_races: int = 24,
    noise_std: float = 0.15
) -> pd.DataFrame:
    """
    Simulate a full F1 season.
    """

    df = model_df.copy()
    df["total_points"] = 0

    for _ in range(n_races):
        race = simulate_race(df, noise_std=noise_std)
        df["total_points"] += race["sim_points"].values

    df = df.sort_values("total_points", ascending=False).reset_index(drop=True)
    df["final_position"] = df.index + 1

    return df[["driver", "total_points", "final_position"]]


# ==========================================================
# MONTE CARLO CHAMPIONSHIP PROBABILITY
# ==========================================================

def simulate_many_seasons(
    model_df: pd.DataFrame,
    n_sims: int = 500,
    n_races: int = 24,
    noise_std: float = 0.15
):
    """
    Monte Carlo simulation returning Top 3 finish probability.
    """

    p1 = []
    p2 = []
    p3 = []

    for _ in range(n_sims):
        season = simulate_season(
            model_df=model_df,
            n_races=n_races,
            noise_std=noise_std
        )

        p1.append(season.iloc[0]["driver"])
        p2.append(season.iloc[1]["driver"])
        p3.append(season.iloc[2]["driver"])

    results = pd.DataFrame({
        "P1": p1,
        "P2": p2,
        "P3": p3
    })

    return {
        "Champion_Prob": results["P1"].value_counts(normalize=True),
        "P2_Prob": results["P2"].value_counts(normalize=True),
        "P3_Prob": results["P3"].value_counts(normalize=True)
    }