from pathlib import Path
import pandas as pd

from statsbomb_pipeline.pipeline.team.team_season_aggregator import aggregate_team_season

TEAM_MATCH_PATH = Path("statsbomb_pipeline/data/processed/team/team_match.parquet")
OUTPUT_PATH = Path("statsbomb_pipeline/data/processed/team/team_season.parquet")


def build_team_season_table():
    print("Loading team-match table...")
    df = pd.read_parquet(TEAM_MATCH_PATH)
    print(f"Loaded {len(df):,} rows.")

    print("Aggregating season-level team stats...")
    team_season = aggregate_team_season(df)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    team_season.to_parquet(OUTPUT_PATH, index=False)
    team_season.to_csv(OUTPUT_PATH.with_suffix(".csv"), index=False)

    print("Saved team-season table:")
    print(f"  {OUTPUT_PATH}")
    print(f"  {OUTPUT_PATH.with_suffix('.csv')}")

    return team_season


if __name__ == "__main__":
    build_team_season_table()
