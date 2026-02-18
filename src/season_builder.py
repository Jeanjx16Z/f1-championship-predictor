import fastf1
import pandas as pd
from pathlib import Path
from tqdm import tqdm

from src.data_loader import build_race_summary

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data" / "processed"
DATA_DIR.mkdir(parents=True, exist_ok=True)

def build_season_dataset(year: int) -> pd.DataFrame:
    schedule = fastf1.get_event_schedule(year)

    races = schedule[schedule['EventFormat'] == 'conventional']

    season_data = []

    for _, event in tqdm(races.iterrows(), total=len(races)):
        gp_name = event['EventName']

        try:
            race_df = build_race_summary(year, gp_name)
            season_data.append(race_df)
        except Exception as e:
            print(f"Failed {gp_name}: {e}")

    season_df =pd.concat(season_data, ignore_index=True)
    return season_df

def save_season_dataset(year: int):
    df = build_season_dataset(year)
    output_path = DATA_DIR / f"season_{year}.csv"
    df.to_csv(output_path, index=False)

    print(f"Saved dataset to: {output_path}")