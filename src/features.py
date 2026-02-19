import pandas as pd

def add_basic_flags(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["is_win"] = (df["finish_position"] == 1).astype(int)
    df["is_podium"] = (df["finish_position"] <= 3).astype(int)
    df["is_tops"] = (df["finish_position"] <= 5).astype(int)

    return df

def add_cumulative_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df= df.sort_values(["driver", "round_number"])

    df["cumulative_points"] = df.groupby("driver")["points"].cumsum()
    df["cumulative_wins"] = df.groupby("driver")["is_win"].cumsum()
    df["cumulative_podiums"] = df.groupby("driver")["is_podium"].cumsum()

    return df

def add_rolling_features(df: pd.DataFrame, window: int = 3) -> pd.DataFrame:
    df =df.copy()

    df["points_momentum"] = (
        df.groupby("driver")["points"]
        .rolling(window=window, min_periods=1)
        .mean()
        .reset_index(level=0, drop=True)
    )

    df["avg_finish_lastN"] = (
        df.groupby("driver")["finish_position"]
        .rolling(window=window, min_periods=1)
        .mean()
        .reset_index(level=0, drop=True)
    )

    return df

def add_consistency_score(df: pd.DataFrame, window: int=5) -> pd.DataFrame:
    df = df.copy()

    # Hitung rata-rata posisi finis dalam 5 balapan terakhir
    df["consistency_score"] = (
        df.groupby("driver")["finish_position"]
        .rolling(window=window, min_periods=1)
        .mean()
        .reset_index(level=0, drop=True)
    )

    return df


def add_championship_gap(df: pd.DataFrame)-> pd.DataFrame:
    df =df.copy()

    #cari leader tiap race
    df["race_leader_points"] = df.groupby("gp")["cumulative_points"].transform("max")
    df["points_gap_to_leader"] = (
        df["race_leader_points"] - df["cumulative_points"]
    )

    return df


def build_features_dataset(df: pd.DataFrame) -> pd.DataFrame:
    df = add_basic_flags(df)
    df = add_cumulative_features(df)
    df = add_rolling_features(df)
    df = add_consistency_score(df)
    df = add_championship_gap(df)

    return df