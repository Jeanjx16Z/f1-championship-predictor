import pandas as pd
import numpy as np

def compute_driver_statistics(df: pd.DataFrame)-> pd.DataFrame:
    df = df.copy()
    stats= df.groupby("driver").agg(
        avg_points = ("points", "mean"),
        avg_finish=("finish_position", "mean"),
        std_finish = ("finish_position", "std"),
        total_races=("gp", "count"),
        wins=("is_win", "sum"),
        podiums=("is_podium", "sum"),
    ).reset_index()

    #Reliability (Finish posistion Nan = DNF)
    dnf_counts = df[df["finish_position"].isna()].groupby("driver").size()
    stats["dnf"] = stats["driver"].map(dnf_counts).fillna(0)
    
    stats["dnf_rate"] = stats["dnf"] / stats["total_races"]
    return stats

def normalize_series(series: pd.Series) -> pd.Series:
    min_val = series.min()
    max_val = series.max()

    if max_val - min_val == 0:
        return pd.Series([0.5] * len(series), index=series.index)

    return (series - min_val) / (max_val - min_val)

def build_driver_rating(stats: pd.DataFrame)->pd.DataFrame:
    stats = stats.copy()

    stats["finish_quality"] = 1 / stats["avg_finish"]
    stats["consistecy"] = 1 / stats["std_finish"]

    #Normalization
    stats["norm_points"] = normalize_series(stats["avg_points"])
    stats["norm_finish"] = normalize_series(stats["finish_quality"])
    stats["norm_consistency"] = normalize_series(stats["consistecy"])
    stats["norm_realibility"] = normalize_series(1 - stats["dnf_rate"])

    #Composite score
    stats["rating"] = (
        0.40 * stats["norm_points"] +
        0.25 * stats["norm_finish"] +
        0.20 * stats["norm_consistency"] +
        0.15 * stats["norm_realibility"]
    )
    return stats.sort_values("rating", ascending=False)