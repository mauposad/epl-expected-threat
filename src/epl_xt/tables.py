"""Build the match, player and team modelling tables from the rated action table.

Every per-action metric is defined once in :func:`add_action_metrics` and then
summed to player-match, player-season, team-match and team-season level.
"""

import json
from pathlib import Path

import numpy as np
import pandas as pd

from epl_xt.events import successful_mask
from epl_xt.pitch import FINAL_THIRD_X, in_box

# Per-action counts and values that are summed when aggregating.
METRICS = [
    "passes",
    "passes_completed",
    "carries",
    "shots",
    "goals",
    "xg",
    "npxg",
    "xt",
    "xt_pass",
    "xt_carry",
    "passes_into_box",
    "box_entries",
    "final_third_entries",
]

# Team metrics that also get an "_against" column (the opponent's value).
TEAM_AGAINST_METRICS = ["shots", "xg", "npxg", "xt", "passes", "box_entries", "final_third_entries"]


def build_matches_table(matches_file: str | Path) -> pd.DataFrame:
    matches = json.loads(Path(matches_file).read_text(encoding="utf-8"))
    df = pd.DataFrame(
        {
            "match_id": m["match_id"],
            "match_date": pd.to_datetime(m["match_date"]),
            "match_week": m["match_week"],
            "home_team_id": m["home_team"]["home_team_id"],
            "home_team": m["home_team"]["home_team_name"],
            "away_team_id": m["away_team"]["away_team_id"],
            "away_team": m["away_team"]["away_team_name"],
            "home_score": m["home_score"],
            "away_score": m["away_score"],
        }
        for m in matches
    )
    return df.sort_values(["match_date", "match_id"]).reset_index(drop=True)


def add_action_metrics(actions: pd.DataFrame) -> pd.DataFrame:
    """Add one 0/1 (or value) column per metric in :data:`METRICS`."""
    a = actions
    is_pass = a["type"] == "Pass"
    is_carry = a["type"] == "Carry"
    is_shot = a["type"] == "Shot"
    successful = successful_mask(a)
    open_play = ~a["set_piece"]
    good_move = (is_pass | is_carry) & successful & open_play

    starts_in_box = in_box(a["x"], a["y"])
    ends_in_box = in_box(a["end_x"], a["end_y"])
    xg = a["xg"].fillna(0.0)

    return a.assign(
        passes=is_pass.astype(int),
        passes_completed=(is_pass & successful).astype(int),
        carries=is_carry.astype(int),
        shots=is_shot.astype(int),
        # Own goals have no shot event, so they never count towards a player
        # or team here; team scores come from the match result instead.
        goals=(is_shot & a["is_goal"]).astype(int),
        xg=xg,
        npxg=np.where(a["is_penalty"], 0.0, xg),
        xt_pass=np.where(is_pass, a["xt"], 0.0),
        xt_carry=np.where(is_carry, a["xt"], 0.0),
        passes_into_box=(good_move & is_pass & ~starts_in_box & ends_in_box).astype(int),
        box_entries=(good_move & ~starts_in_box & ends_in_box).astype(int),
        final_third_entries=(good_move & (a["x"] < FINAL_THIRD_X) & (a["end_x"] >= FINAL_THIRD_X)).astype(
            int
        ),
    )


# ----------------------------------------------------------------------------
# Players
# ----------------------------------------------------------------------------


def build_player_match_table(actions: pd.DataFrame, minutes: pd.DataFrame) -> pd.DataFrame:
    """One row per player per match they played in, with minutes and summed metrics."""
    keys = ["match_id", "team_id", "player_id"]
    sums = actions.dropna(subset=["player_id"]).groupby(keys)[METRICS].sum().reset_index()
    sums["player_id"] = sums["player_id"].astype(int)
    df = minutes.merge(sums, on=keys, how="left")
    df[METRICS] = df[METRICS].fillna(0)
    return df


def build_player_season_table(player_match: pd.DataFrame) -> pd.DataFrame:
    """One row per player per team, with season totals and per-90 rates.

    The listed position is the one the player spent the most minutes in.
    """
    keys = ["player_id", "team_id"]
    totals = player_match.groupby(keys).agg(
        player=("player", "first"),
        team=("team", "first"),
        matches=("match_id", "nunique"),
        starts=("started", "sum"),
        minutes=("minutes", "sum"),
        **{m: (m, "sum") for m in METRICS},
    )

    by_position = player_match.groupby(keys + ["position"])["minutes"].sum().reset_index()
    primary = by_position.sort_values("minutes").groupby(keys).tail(1).set_index(keys)["position"]
    totals["position"] = primary
    group_of = player_match.drop_duplicates("position").set_index("position")["position_group"]
    totals["position_group"] = totals["position"].map(group_of)

    nineties = totals["minutes"] / 90.0
    for m in METRICS:
        totals[f"{m}_p90"] = totals[m] / nineties
    totals["pass_completion"] = totals["passes_completed"] / totals["passes"].replace(0, np.nan)

    return totals.reset_index().sort_values("minutes", ascending=False, ignore_index=True)


# ----------------------------------------------------------------------------
# Teams
# ----------------------------------------------------------------------------


def build_team_match_table(actions: pd.DataFrame, matches: pd.DataFrame) -> pd.DataFrame:
    """One row per team per match: own metrics, opponent metrics and the result."""
    sums = actions.groupby(["match_id", "team_id"])[METRICS].sum().reset_index()
    sums = sums.drop(columns="goals")  # use the official score, which includes own goals

    home = matches.rename(
        columns={
            "home_team_id": "team_id",
            "home_team": "team",
            "away_team_id": "opponent_id",
            "away_team": "opponent",
            "home_score": "goals_for",
            "away_score": "goals_against",
        }
    ).assign(is_home=True)
    away = matches.rename(
        columns={
            "away_team_id": "team_id",
            "away_team": "team",
            "home_team_id": "opponent_id",
            "home_team": "opponent",
            "away_score": "goals_for",
            "home_score": "goals_against",
        }
    ).assign(is_home=False)
    cols = [
        "match_id",
        "match_date",
        "match_week",
        "team_id",
        "team",
        "opponent_id",
        "opponent",
        "is_home",
        "goals_for",
        "goals_against",
    ]
    fixtures = pd.concat([home[cols], away[cols]], ignore_index=True)

    df = fixtures.merge(sums, on=["match_id", "team_id"], how="left")
    opp = sums[["match_id", "team_id"] + TEAM_AGAINST_METRICS].rename(
        columns={"team_id": "opponent_id", **{m: f"{m}_against" for m in TEAM_AGAINST_METRICS}}
    )
    df = df.merge(opp, on=["match_id", "opponent_id"], how="left")

    df["result"] = np.select(
        [df["goals_for"] > df["goals_against"], df["goals_for"] < df["goals_against"]],
        ["W", "L"],
        default="D",
    )
    df["points"] = df["result"].map({"W": 3, "D": 1, "L": 0})
    df["pass_completion"] = df["passes_completed"] / df["passes"]
    return df.sort_values(
        ["match_date", "match_id", "is_home"], ascending=[True, True, False], ignore_index=True
    )


def build_team_season_table(team_match: pd.DataFrame) -> pd.DataFrame:
    """One row per team: league record, season totals, per-match rates and differentials."""
    sum_cols = (
        ["goals_for", "goals_against", "points"]
        + [m for m in METRICS if m != "goals"]
        + [f"{m}_against" for m in TEAM_AGAINST_METRICS]
    )
    g = team_match.groupby(["team_id", "team"])
    df = g[sum_cols].sum()
    df.insert(0, "matches", g.size())
    for r, col in [("W", "wins"), ("D", "draws"), ("L", "losses")]:
        df.insert(df.columns.get_loc("goals_for"), col, g["result"].apply(lambda s, r=r: (s == r).sum()))
    df = df.reset_index()

    df["goal_diff"] = df["goals_for"] - df["goals_against"]
    df["xg_diff"] = df["xg"] - df["xg_against"]
    df["npxg_diff"] = df["npxg"] - df["npxg_against"]
    df["xt_diff"] = df["xt"] - df["xt_against"]
    df["pass_completion"] = df["passes_completed"] / df["passes"]

    per_match = [
        "goals_for",
        "goals_against",
        "points",
        "shots",
        "xg",
        "npxg",
        "xt",
        "xg_against",
        "xt_against",
        "passes",
        "box_entries",
        "final_third_entries",
    ]
    for c in per_match:
        df[f"{c}_pm"] = df[c] / df["matches"]

    df = df.sort_values(["points", "goal_diff", "goals_for"], ascending=False, ignore_index=True)
    df.insert(0, "rank", np.arange(1, len(df) + 1))
    return df
