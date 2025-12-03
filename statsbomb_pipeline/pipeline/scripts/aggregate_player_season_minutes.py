import pandas as pd
from pathlib import Path
from collections import Counter


BASE_DIR = Path(__file__).resolve().parents[2]  # statsbomb_pipeline/
DATA_PROCESSED = BASE_DIR / "data" / "processed"

MINUTES_FILE = DATA_PROCESSED / "player_minutes_2015_2016.csv"
OUTPUT_FILE = DATA_PROCESSED / "player_season_minutes_2015_2016.csv"


def mode_or_first(series):
    """Return the most common non-null value in a Series, or None."""
    vals = [v for v in series if pd.notna(v)]
    if not vals:
        return None
    counts = Counter(vals)
    return counts.most_common(1)[0][0]


def aggregate_player_season_minutes():
    # Load per-match player minutes
    df = pd.read_csv(MINUTES_FILE)

    # Consider only matches where player actually played
    df_active = df[df["minutes_played"] > 0].copy()

    # Group by player_id
    grouped = df_active.groupby("player_id")

    agg_rows = []

    for pid, g in grouped:
        player_name = mode_or_first(g["player_name"])
        team_id = mode_or_first(g["team_id"])
        team_name = mode_or_first(g["team_name"])
        position = mode_or_first(g["position"])

        minutes_played_total = g["minutes_played"].sum()

        matches_played = g["match_id"].nunique()
        starts = g[g["is_starter"] == True]["match_id"].nunique()
        sub_appearances = matches_played - starts

        # Full 90s (allow 작은 float noise, e.g., 89.5+)
        full_90s = (g["minutes_played"] >= 89.5).sum()

        minutes_per_match = (
            minutes_played_total / matches_played if matches_played > 0 else 0.0
        )

        agg_rows.append(
            {
                "player_id": pid,
                "player_name": player_name,
                "team_id": team_id,
                "team_name": team_name,
                "position": position,
                "matches_played": matches_played,
                "starts": starts,
                "sub_appearances": sub_appearances,
                "full_90s": full_90s,
                "minutes_played_total": minutes_played_total,
                "minutes_per_match": minutes_per_match,
            }
        )

    season_df = pd.DataFrame(agg_rows)
    season_df.sort_values("minutes_played_total", ascending=False, inplace=True)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    season_df.to_csv(OUTPUT_FILE, index=False)

    print(f"Saved player-season minutes → {OUTPUT_FILE}")
    print(season_df.head(30))
    return season_df


if __name__ == "__main__":
    aggregate_player_season_minutes()
