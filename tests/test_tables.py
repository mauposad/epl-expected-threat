import pandas as pd
import pytest

from epl_xt.tables import add_action_metrics, build_team_match_table, build_team_season_table


def act(
    team_id,
    type_,
    x,
    y,
    end_x=None,
    end_y=None,
    successful=True,
    xg=None,
    is_goal=False,
    is_penalty=False,
    set_piece=False,
):
    return {
        "match_id": 1,
        "team_id": team_id,
        "player_id": team_id * 10,
        "type": type_,
        "x": x,
        "y": y,
        "end_x": end_x,
        "end_y": end_y,
        "successful": successful if type_ != "Shot" else None,
        "xg": xg,
        "is_goal": is_goal,
        "is_penalty": is_penalty,
        "set_piece": set_piece,
        "xt": 0.0,
    }


@pytest.fixture
def matches():
    # Home team won 2-1, but one of their goals was an own goal (no shot event).
    return pd.DataFrame(
        [
            {
                "match_id": 1,
                "match_date": pd.Timestamp("2015-08-08"),
                "match_week": 1,
                "home_team_id": 1,
                "home_team": "Home",
                "away_team_id": 2,
                "away_team": "Away",
                "home_score": 2,
                "away_score": 1,
            }
        ]
    )


@pytest.fixture
def actions():
    rows = [
        act(1, "Shot", 108, 40, xg=0.4, is_goal=True),
        act(1, "Shot", 108, 40, xg=0.76, is_penalty=True, set_piece=True),
        act(1, "Pass", 70, 40, 90, 40),  # final third entry
        act(1, "Pass", 85, 40, 110, 40),  # pass into box
        act(1, "Pass", 85, 40, 110, 40, set_piece=True),  # corner: not counted
        act(1, "Carry", 90, 40, 105, 40),  # carry into box
        act(1, "Pass", 70, 40, 90, 40, successful=False),  # failed: not counted
        act(2, "Shot", 108, 40, xg=0.2, is_goal=True),
    ]
    return add_action_metrics(pd.DataFrame(rows))


def test_action_metrics(actions):
    home = actions[actions["team_id"] == 1].sum(numeric_only=True)
    assert home["final_third_entries"] == 1
    assert home["passes_into_box"] == 1
    assert home["box_entries"] == 2
    assert home["passes_completed"] == 3
    assert home["xg"] == pytest.approx(1.16)
    assert home["npxg"] == pytest.approx(0.4)


def test_team_match_uses_official_score(actions, matches):
    tm = build_team_match_table(actions, matches).set_index("team_id")
    # Only one home shot was a goal, but the own goal still counts.
    assert tm.loc[1, "goals_for"] == 2
    assert tm.loc[1, "result"] == "W" and tm.loc[1, "points"] == 3
    assert tm.loc[2, "result"] == "L" and tm.loc[2, "points"] == 0
    assert tm.loc[2, "xg_against"] == pytest.approx(1.16)
    assert bool(tm.loc[1, "is_home"]) and not bool(tm.loc[2, "is_home"])


def test_team_season_rank(actions, matches):
    ts = build_team_season_table(build_team_match_table(actions, matches))
    assert ts.loc[0, "team"] == "Home"
    assert ts.loc[0, ["rank", "wins", "points", "goal_diff"]].tolist() == [1, 1, 3, 1]
