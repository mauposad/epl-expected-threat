import pandas as pd
from pathlib import Path

MINUTES = Path("statsbomb_pipeline/data/processed/player_minutes_2015_2016.csv")
XTHREAT = Path("statsbomb_pipeline/data/processed/xthreat_player_match.parquet")
OUTPUT = Path("statsbomb_pipeline/data/processed/player_match_model_data.csv")


def merge_minutes_xThreat():

    df_min = pd.read_csv(MINUTES)
    df_xt = pd.read_parquet(XTHREAT)

    merged = df_min.merge(df_xt, on=["player_id", "match_id", "team_id"], how="left")

    # Replace NaN xThreat with 0 (players who played but had no Pass/Carry)
    merged.fillna(
        {"xThreat_total": 0, "xThreat_pass": 0, "xThreat_carry": 0, "xg_total": 0}, inplace=True
    )

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    merged.to_csv(OUTPUT, index=False)

    print(f"✓ Saved full player-match dataset → {OUTPUT}")


if __name__ == "__main__":
    merge_minutes_xThreat()
