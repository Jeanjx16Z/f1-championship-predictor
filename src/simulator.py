import pandas as pd
import numpy as np

F1_POINTS = [25, 18, 15, 12, 10, 8, 6, 4, 2, 1] 

def simulate_race(driver_df: pd.DataFrame, noise_std: float= 0.07) -> pd.DataFrame:
    df = driver_df.copy()

    #Generate performance score (skill + noise)
    df["performance_score"] = (
        df["rating"] + 
        np.random.normal(0, noise_std, size=len(df))
    )

    #Generate DNF event
    random_vals = np.random.rand(len(df))
    df["dnf_flag"] = random_vals < df["dnf_rate"]

    #Sort by performance score
    df = df.sort_values("performance_score", ascending=False).reset_index(drop=True)

    #Assign provisional finish position
    df["sim_finish_position"] = np.arange(1, len(df) + 1)

    #Push DNF drivers to bottom
    if df["dnf_flag"].any():
        dnf_drivers = df[df["dnf_flag"]].copy()
        non_dnf = df[~df["dnf_flag"]].copy()

        non_dnf["sim_finish_position"] = np.arange(1, len(non_dnf) + 1)
        dnf_drivers["sim_finish_position"] = np.arange(
            len(non_dnf) + 1, len(df) + 1
        )


        df = pd.concat([non_dnf, dnf_drivers]).reset_index(drop=True)

    #Assign points
    df["sim_points"] = 0
    for i in range(min(len(F1_POINTS), len(df))):
        df.loc[i, "sim_points"] = F1_POINTS[i]

    return df.sort_values("sim_finish_position").reset_index(drop=True)