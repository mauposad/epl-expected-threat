import pandas as pd
from pathlib import Path

MERGED = Path("statsbomb_pipeline/data/processed/player_match_model_data.parquet")
OUTPUT = Path("statsbomb_pipeline/data/processed/player_season_model_dataset.csv")


def build_season_dataset():
    print("Loading merged player-match dataset...")
    df = pd.read_parquet(MERGED)

    # -----------------------------------------------------------
    # 1. Clean and normalize columns
    # -----------------------------------------------------------

    # Use player_name_x unless missing, else fallback to player_name_y
    df["player_name"] = df["player_name_x"].fillna(df["player_name_y"])

    # Some subs have missing start_min/end_min — fix minutes calculation
    df["minutes_played"] = df["minutes_played"].fillna(0)

    # Position may be empty for subs or GK edge cases
    df["position"] = df["position"].fillna("Unknown")

    # Mark match played (any minutes > 0 means appearance)
    df["match_played_flag"] = (df["minutes_played"] > 0).astype(int)

    # -----------------------------------------------------------
    # 2. Aggregate per-player season totals
    # -----------------------------------------------------------

    season = (
        df.groupby(["player_id", "player_name", "team_id", "team_name", "position"])
        .agg(
            minutes_played_total=("minutes_played", "sum"),
            matches_played=("match_played_flag", "sum"),
            xThreat_total=("xThreat_total", "sum"),
            xThreat_pass_total=("xThreat_pass", "sum"),
            xThreat_carry_total=("xThreat_carry", "sum"),
            xg_total=("xg_total", "sum"),
        )
        .reset_index()
    )

    # -----------------------------------------------------------
    # 3. Compute per 90 metrics
    # -----------------------------------------------------------

    season["minutes_90s"] = season["minutes_played_total"] / 90.0

    # Avoid divide-by-zero
    season["minutes_90s"] = season["minutes_90s"].replace({0: 1e-9})

    season["xThreat_per90"] = season["xThreat_total"] / season["minutes_90s"]
    season["xThreat_pass_per90"] = season["xThreat_pass_total"] / season["minutes_90s"]
    season["xThreat_carry_per90"] = season["xThreat_carry_total"] / season["minutes_90s"]

    # Fill remaining NaNs
    season = season.fillna(0)

    # -----------------------------------------------------------
    # 4. Save final dataset
    # -----------------------------------------------------------

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    season.to_csv(OUTPUT, index=False)

    print(f"✓ Saved season-level dataset → {OUTPUT}")
    print("Preview:")
    print(season.head())


if __name__ == "__main__":
    build_season_dataset()
