import pandas as pd


def aggregate_team_season(team_match_df: pd.DataFrame) -> pd.DataFrame:
    """
    Produce a season-level table (1 row per team),
    aggregated from team-match-level metrics.
    """

    df = team_match_df.copy()

    # Convert outcome to numeric flags
    df["win"] = (df["outcome"] == "win").astype(int)
    df["draw"] = (df["outcome"] == "draw").astype(int)
    df["loss"] = (df["outcome"] == "loss").astype(int)

    # Aggregate season totals per team
    agg = (
        df.groupby(["team_id", "team_name"])
        .agg(
            matches_played=("match_id", "nunique"),
            wins=("win", "sum"),
            draws=("draw", "sum"),
            losses=("loss", "sum"),
            goals_for=("goals", "sum"),
            goals_against=("opponent_goals", "sum"),
            shots_for=("shots", "sum"),
            passes_for=("passes", "sum"),
            carries_for=("carries", "sum"),
            ppa_for=("team_ppa", "sum"),
            f3_entries_for=("final_third_entries", "sum"),
            xg_for=("team_xg", "sum"),
            xthreat_for=("team_xthreat", "sum"),
        )
        .reset_index()
    )

    # Derived metrics
    agg["goal_diff"] = agg["goals_for"] - agg["goals_against"]
    agg["xg_per_match"] = agg["xg_for"] / agg["matches_played"]
    agg["xthreat_per_match"] = agg["xthreat_for"] / agg["matches_played"]
    agg["goals_per_match"] = agg["goals_for"] / agg["matches_played"]
    agg["ppa_per_match"] = agg["ppa_for"] / agg["matches_played"]
    agg["f3_entries_per_match"] = agg["f3_entries_for"] / agg["matches_played"]

    return agg
