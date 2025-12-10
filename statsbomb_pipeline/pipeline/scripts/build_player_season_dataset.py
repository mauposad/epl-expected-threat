import pandas as pd
from pathlib import Path

MERGED = Path("statsbomb_pipeline/data/processed/second/player_match_model_data.csv")
OUTPUT = Path("statsbomb_pipeline/data/processed/player_season_model_dataset.csv")


def build_season_dataset():
    print("Loading merged player-match dataset...")
    df = pd.read_csv(MERGED)

    # -----------------------------------------------------------
    # 1. Clean and normalize columns
    # -----------------------------------------------------------

    # Use player_name_x unless missing, else fallback to player_name_y
    df["player_name"] = df["player_name_x"].fillna(df["player_name_y"])

    # After A1 fixes, minutes_played should never be NaN or zero.
    df = df[df["minutes_played"] >= 1.0].copy()

    # Drop rows with missing position (should be none now)
    df = df.dropna(subset=["position"])

    # Mark match played (any minutes > 0 means appearance)
    df["match_played_flag"] = 1
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
    # Step 3.  Collapse to ONE ROW per player per team
    # -----------------------------------------------------------
    print("Collapsing positional rows into a single player-season entry...")

    # Step 1: choose primary position (where the player played the most minutes)
    primary_positions = (
        season.sort_values("minutes_played_total", ascending=False)
        .groupby(["player_id", "team_id"], as_index=False)
        .first()[["player_id", "team_id", "position"]]
        .rename(columns={"position": "primary_position"})
    )

    # aggregate totals across *all* positions
    collapsed = season.groupby(
        ["player_id", "player_name", "team_id", "team_name"], as_index=False
    ).agg(
        minutes_played_total=("minutes_played_total", "sum"),
        matches_played=("matches_played", "sum"),
        xThreat_total=("xThreat_total", "sum"),
        xThreat_pass_total=("xThreat_pass_total", "sum"),
        xThreat_carry_total=("xThreat_carry_total", "sum"),
        xg_total=("xg_total", "sum"),
    )

    # Step 3 cont: attach the chosen primary position
    collapsed = collapsed.merge(primary_positions, on=["player_id", "team_id"], how="left")
    collapsed = collapsed.rename(columns={"primary_position": "position"})

    # Replace the original `season` df
    season = collapsed

    # -----------------------------------------------------------
    # 4. Compute per 90 metrics
    # -----------------------------------------------------------

    season["minutes_90s"] = season["minutes_played_total"] / 90.0

    season["xThreat_per90"] = season["xThreat_total"] / season["minutes_90s"]
    season["xThreat_pass_per90"] = season["xThreat_pass_total"] / season["minutes_90s"]
    season["xThreat_carry_per90"] = season["xThreat_carry_total"] / season["minutes_90s"]

    # Fill remaining NaNs
    season = season.fillna(0)

    # -----------------------------------------------------------
    # 5. Save final dataset
    # -----------------------------------------------------------

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    season.to_csv(OUTPUT, index=False)

    print(f"✓ Saved season-level dataset → {OUTPUT}")
    print("Preview:")
    print(season.head())


if __name__ == "__main__":
    build_season_dataset()
