"""
Docstring for statsbomb_pipeline.script
Sanity checks as we move through the project
"""

# sanity_checks.py
# Run this from: /home/mauposad/CS-Projects/data-mine-mposadas
# Example: python sanity_checks.py

import pandas as pd
from pathlib import Path

# -----------------------------
# CONFIG — update if needed
# -----------------------------
EVENTS_DIR = Path("statsbomb_pipeline/data/processed/xthreat_events")
PLAYER_MATCH_XT = Path("statsbomb_pipeline/data/processed/xthreat_player_match.parquet")
MINUTES = Path("statsbomb_pipeline/data/processed/player_minutes_2015_2016.csv")
MERGED = Path("statsbomb_pipeline/data/processed/player_match_model_data.parquet")
SEASON = Path("statsbomb_pipeline/data/processed/player_season_model_dataset.parquet")


# ============================================================
# HELPER PRINTER
# ============================================================


def title(msg):
    print("\n" + "=" * 70)
    print(msg)
    print("=" * 70 + "\n")


# ============================================================
# PHASE 1 — EVENT-LEVEL xTHREAT SANITY CHECKS
# ============================================================


def check_event_level():
    title("PHASE 1 — Event-level xThreat Checks")

    sample_file = next(EVENTS_DIR.glob("*.parquet"))
    print(f"Loading sample event file: {sample_file}")
    df = pd.read_parquet(sample_file)

    print("HEAD:")
    print(df.head(), "\n")

    print("Columns:", df.columns.tolist(), "\n")

    # Required columns
    required = {
        "event_type",
        "player_id",
        "team_id",
        "xThreat",
        "match_id",
        "x",
        "y",
        "end_x",
        "end_y",
    }
    missing = required - set(df.columns)
    print("Missing required columns:", missing)

    # Negative xThreat?
    print("Negative xThreat count:", (df["xThreat"] < 0).sum())

    # Coordinate bounds
    invalid_coords = df[(df["x"] < 0) | (df["x"] > 120) | (df["y"] < 0) | (df["y"] > 80)]
    print("Invalid coordinate rows:", len(invalid_coords))

    # Zone bounds
    print("start_zone range:", df["start_zone"].min(), "→", df["start_zone"].max())
    print("end_zone range:", df["end_zone"].min(), "→", df["end_zone"].max())


# ============================================================
# PHASE 2 — PLAYER-MATCH xTHREAT SANITY CHECKS
# ============================================================


def check_player_match_xThreat():
    title("PHASE 2 — Player-match xThreat Checks")

    df = pd.read_parquet(PLAYER_MATCH_XT)

    print("Shape:", df.shape)
    print(df.head(), "\n")

    # Unique per player per match
    dupes = df[df.duplicated(["player_id", "match_id"], keep=False)]
    print("Duplicate (player_id, match_id) rows:", len(dupes))

    # Missing xThreat?
    print("NA counts:")
    print(df[["xThreat_total", "xThreat_pass", "xThreat_carry"]].isna().sum())

    print("\nDistribution of xThreat_total:")
    print(df["xThreat_total"].describe())

    print("\nPlayers per match (example):")
    print(df.groupby("match_id").size().head())


# ============================================================
# PHASE 3 — MINUTES SANITY CHECKS
# ============================================================


def check_minutes():
    title("PHASE 3 — Minutes Played Checks")

    df = pd.read_csv(MINUTES)

    print("Shape:", df.shape)
    print(df.head())

    # Team minutes ≈ 990
    team_minutes = df.groupby(["match_id", "team_id"])["minutes_played"].sum()
    print("\nTeam minutes summary:")
    print(team_minutes.describe())

    # Active players per match
    active = df[df["minutes_played"] > 0]
    players_per_team = active.groupby(["match_id", "team_id"]).size()
    print("\nPlayers with minutes per team:")
    print(players_per_team.describe())

    # Invalid minutes?
    print("\nMinutes < 0 or > 120:")
    print(df[(df["minutes_played"] < 0) | (df["minutes_played"] > 120)])


# ============================================================
# PHASE 4 — MERGED MINUTES + xTHREAT SANITY CHECKS
# ============================================================


def check_merged():
    title("PHASE 4 — Merged minutes + xThreat Checks")

    df = pd.read_parquet(MERGED)

    print("Shape:", df.shape)
    print(df.head(), "\n")

    print("NA counts:")
    print(df.isna().sum())

    # Players with xThreat=0 should still have minutes
    print("\nPlayers with 0 xThreat:")
    print(df[df["xThreat_total"] == 0]["minutes_played"].describe())

    # Total minutes per match should ≈ 1980
    total_minutes = df.groupby("match_id")["minutes_played"].sum()
    print("\nTotal minutes per match:")
    print(total_minutes.describe())


# ============================================================
# PHASE 5 — SEASON AGGREGATION SANITY CHECKS
# ============================================================


def check_season():
    title("PHASE 5 — Season-level Aggregation Checks")

    df = pd.read_parquet(SEASON)

    print("Shape:", df.shape)
    print(df.head(), "\n")

    # Duplicate players?
    dupes = df[df.duplicated("player_id", keep=False)]
    print("Duplicate player_id rows:", len(dupes))

    # Per 90 stats
    for col in ["xThreat_per90", "xThreat_pass_per90", "xThreat_carry_per90"]:
        if col in df.columns:
            print(f"\n{col} distribution:")
            print(df[col].describe())

    # Missing positions?
    print("\nPlayers missing position field:")
    print(df[df["position"].isna()]["player_name"].unique()[:20])


# ============================================================
# RUN ALL CHECKS
# ============================================================

if __name__ == "__main__":
    check_event_level()
    check_player_match_xThreat()
    check_minutes()
    check_merged()
    check_season()

    print("\nALL SANITY CHECKS COMPLETE.\n")
