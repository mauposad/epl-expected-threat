import json

import pytest

from epl_xt.minutes import player_minutes, position_group


@pytest.mark.parametrize(
    "position, group",
    [
        ("Goalkeeper", "GK"),
        ("Left Center Back", "DEF"),
        ("Right Wing Back", "DEF"),
        ("Center Defensive Midfield", "MID"),
        ("Left Midfield", "MID"),
        ("Right Wing", "FWD"),
        ("Secondary Striker", "FWD"),
        (None, None),
    ],
)
def test_position_group(position, group):
    assert position_group(position) == group


def spell(position, start, end, reason="Starting XI"):
    return {"position": position, "from": start, "to": end, "start_reason": reason}


def test_player_minutes(tmp_path):
    lineup = [
        {
            "team_id": 1,
            "team_name": "Home",
            "lineup": [
                # Full match, moved position at 60'.
                {
                    "player_id": 10,
                    "player_name": "A",
                    "positions": [
                        spell("Center Forward", "00:00", "60:00"),
                        spell("Right Wing", "60:00", None),
                    ],
                },
                # Treatment break: off 20:00-20:30, then back on.
                {
                    "player_id": 11,
                    "player_name": "B",
                    "positions": [
                        spell("Left Back", "00:00", "20:00"),
                        spell("Left Back", "20:30", None, "Player On"),
                    ],
                },
                # Substitute on at 80:00.
                {
                    "player_id": 12,
                    "player_name": "C",
                    "positions": [spell("Center Forward", "80:00", None, "Substitution - On (Tactical)")],
                },
                # Unused substitute.
                {"player_id": 13, "player_name": "D", "positions": []},
            ],
        }
    ]
    path = tmp_path / "123.json"
    path.write_text(json.dumps(lineup))

    df = player_minutes(path, match_end=94.5).set_index("player_id")

    assert list(df.index) == [10, 11, 12]
    assert df.loc[10, "minutes"] == pytest.approx(94.5)
    assert df.loc[10, "position"] == "Center Forward"  # 60 minutes there vs 34.5 on the wing
    assert df.loc[11, "minutes"] == pytest.approx(94.0)
    assert df.loc[12, "minutes"] == pytest.approx(14.5)
    assert not df.loc[12, "started"]
    assert (df["match_id"] == 123).all()
