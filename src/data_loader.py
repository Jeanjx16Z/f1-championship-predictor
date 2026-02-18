import fastf1
import pandas as pd
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
CACHE_DIR = ROOT_DIR / 'cache'
CACHE_DIR.mkdir(parents=True,exist_ok=True)

fastf1.Cache.enable_cache(CACHE_DIR)
print(f"Cache directory set to: {CACHE_DIR}")

def load_race_session(year: int, gp: str):
#LOAD DATA REACE PERSESI  DARI HASIL DAN LAP DARI FASTF1
    session = fastf1.get_session(year, gp, 'R')
    session.load()
    
    results = session.results.copy()
    laps = session.laps.copy()

    return session, results, laps

def build_race_summary(year: int, gp: str) -> pd.DataFrame:
    session, results, laps = load_race_session(year, gp)

    summary = []
    possible_team_cols = ['TeamName', 'Team', 'Constructor']
    team_col = next((c for c in possible_team_cols if c in results.columns), None)

    for drv in results['Abbreviation']:
        driver_laps = laps.pick_driver(drv)

        summary.append({
            "year": year,
            "gp": gp,
            "driver": drv,
            "team": results.loc[results['Abbreviation'] == drv, team_col].values[0] if team_col else "Unknown",
            "finish_position": results.loc[results['Abbreviation'] == drv, 'Position'].values[0],
            "points": results.loc[results['Abbreviation'] == drv, 'Points'].values[0],
            "avg_lap_time": driver_laps['LapTime'].mean() if not driver_laps.empty else None,
            "fastest_lap": driver_laps['LapTime'].min() if not driver_laps.empty else None,
            "laps_completed": len(driver_laps)
        })

    return pd.DataFrame(summary)
