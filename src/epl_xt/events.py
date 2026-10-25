"""Flatten raw StatsBomb event files into a tidy table of on-ball actions.

Only the three action types used for xT and the derived metrics are kept:
passes, carries and shots.
"""

import json
from pathlib import Path

import numpy as np
import pandas as pd

# StatsBomb pass types that restart play. Everything else (no type, Recovery,
# Interception) is an open-play pass.
SET_PIECE_PASS_TYPES = {"Corner", "Free Kick", "Goal Kick", "Kick Off", "Throw-in"}

ACTION_TYPES = {"Pass", "Carry", "Shot"}


def successful_mask(actions: pd.DataFrame) -> np.ndarray:
    """``successful`` as a plain bool array, with missing values (shots) as False."""
    return actions["successful"].to_numpy(dtype=bool, na_value=False)


def _name(obj: dict | None) -> str | None:
    return obj.get("name") if obj else None


def parse_events(path: str | Path) -> pd.DataFrame:
    """Parse one match's event JSON into one row per pass, carry or shot."""
    path = Path(path)
    match_id = int(path.stem)
    events = json.loads(path.read_text(encoding="utf-8"))

    rows = []
    for e in events:
        etype = _name(e.get("type"))
        if etype not in ACTION_TYPES:
            continue

        start = e.get("location") or [None, None]
        row = {
            "match_id": match_id,
            "event_id": e["id"],
            "index": e["index"],
            "period": e["period"],
            "minute": e["minute"],
            "second": e["second"],
            "possession": e.get("possession"),
            "team_id": e["team"]["id"],
            "team": e["team"]["name"],
            "player_id": e.get("player", {}).get("id"),
            "player": e.get("player", {}).get("name"),
            "play_pattern": _name(e.get("play_pattern")),
            "type": etype,
            "x": start[0],
            "y": start[1],
            "end_x": None,
            "end_y": None,
            "outcome": None,
            "successful": None,
            "set_piece": False,
            "xg": None,
            "is_goal": False,
            "is_penalty": False,
        }

        if etype == "Pass":
            p = e["pass"]
            end = p.get("end_location") or [None, None]
            pass_type = _name(p.get("type"))
            row.update(
                end_x=end[0],
                end_y=end[1],
                outcome=_name(p.get("outcome")),
                # StatsBomb leaves the outcome blank for completed passes.
                successful="outcome" not in p,
                set_piece=pass_type in SET_PIECE_PASS_TYPES,
            )
        elif etype == "Carry":
            end = e["carry"].get("end_location") or [None, None]
            row.update(end_x=end[0], end_y=end[1], successful=True)
        else:
            s = e["shot"]
            outcome = _name(s.get("outcome"))
            shot_type = _name(s.get("type"))
            row.update(
                outcome=outcome,
                xg=s.get("statsbomb_xg"),
                is_goal=outcome == "Goal",
                is_penalty=shot_type == "Penalty",
                set_piece=shot_type in {"Penalty", "Free Kick", "Corner"},
            )

        rows.append(row)

    df = pd.DataFrame(rows)
    df["successful"] = df["successful"].astype("boolean")
    return df
