import pandas as pd


def add_event_flags(events: pd.DataFrame) -> pd.DataFrame:
    """
    Add boolean flags needed to compute team-level match metrics.
    Assumes events come from the custom events_parser.
    """
    df = events.copy()

    # Basic type flags
    df["is_shot"] = df["event_type"] == "Shot"
    df["is_pass"] = df["event_type"] == "Pass"
    df["is_carry"] = df["event_type"] == "Carry"

    # Goals
    df["is_goal"] = df["is_shot"] & (df["outcome"] == "Goal")

    # Pass success: StatsBomb uses outcome=None for success
    df["is_successful_pass"] = df["is_pass"] & (
        df["outcome"].isna() | (df["outcome"] == "Successful")
    )

    # Passes into the penalty area (PPA)
    df["is_ppa"] = (
        df["is_successful_pass"] & (df["end_x"] > 102) & (df["end_y"] > 18) & (df["end_y"] < 62)
    )

    # Final third entries (pass/carry entering final third)
    df["is_final_third_entry"] = False
    df.loc[df["is_successful_pass"] & (df["end_x"] >= 80), "is_final_third_entry"] = True
    df.loc[df["is_carry"] & (df["end_x"] >= 80), "is_final_third_entry"] = True

    return df


def aggregate_team_match(events_with_flags: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate event-level metrics to team-level match metrics.
    Returns one row per (match_id, team_id).
    """

    df = events_with_flags

    group_cols = ["match_id", "team_id"]

    # Aggregate core metrics
    agg = (
        df.groupby(group_cols)
        .agg(
            goals=("is_goal", "sum"),
            shots=("is_shot", "sum"),
            passes=("is_pass", "sum"),
            carries=("is_carry", "sum"),
            team_ppa=("is_ppa", "sum"),
            final_third_entries=("is_final_third_entry", "sum"),
            team_xg=("xg", "sum"),  # Shots-only column
            team_xthreat=("xThreat", "sum"),  # Will exist after merging xThreat outputs
            team_name=("team", "first"),
        )
        .reset_index()
    )

    # Attach opponent info + match outcome classification
    agg = _attach_opponent_and_outcome(agg)

    return agg


def _attach_opponent_and_outcome(team_match: pd.DataFrame) -> pd.DataFrame:
    """
    Adds opponent_id, opponent_goals, and outcome to the team-level match table.
    Assumes exactly two teams per match.
    """
    df = team_match.copy()

    # Self-merge by match to get opponent info
    opponent = df[["match_id", "team_id", "goals"]].rename(
        columns={"team_id": "opponent_id", "goals": "opponent_goals"}
    )

    df = df.merge(opponent, on="match_id", how="left")

    # Drop rows where team_id == opponent_id (self-join artifacts)
    df = df[df["team_id"] != df["opponent_id"]].copy()

    # Determine outcome
    df["outcome"] = "draw"
    df.loc[df["goals"] > df["opponent_goals"], "outcome"] = "win"
    df.loc[df["goals"] < df["opponent_goals"], "outcome"] = "loss"

    return df
