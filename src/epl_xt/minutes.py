"""Minutes played per player per match, from StatsBomb lineup files.

Each lineup entry lists the "spells" a player spent at a position. Times are on
the match clock ("MM:SS"); a spell with no end time lasts until the final
whistle, which is taken from the last event of the match so stoppage time
counts.
"""

import json
from collections import defaultdict
from pathlib import Path

import pandas as pd

POSITION_GROUPS = ("GK", "DEF", "MID", "FWD")


def position_group(position: str | None) -> str | None:
    """Collapse StatsBomb's 24 positions into GK / DEF / MID / FWD."""
    if not position:
        return None
    if position == "Goalkeeper":
        return "GK"
    if "Back" in position:  # includes wing backs
        return "DEF"
    if "Midfield" in position:
        return "MID"
    return "FWD"  # wings, forwards, strikers


def clock_to_minutes(clock: str) -> float:
    mm, ss = clock.split(":")
    return int(mm) + int(ss) / 60.0


def match_end_minute(events: list[dict]) -> float:
    """Match clock at the last event, i.e. the final whistle including stoppage time."""
    return max(e["minute"] + e["second"] / 60.0 for e in events)


def player_minutes(lineup_path: str | Path, match_end: float) -> pd.DataFrame:
    """One row per player who featured in the match, with minutes and primary position."""
    lineup_path = Path(lineup_path)
    match_id = int(lineup_path.stem)
    lineups = json.loads(lineup_path.read_text(encoding="utf-8"))

    rows = []
    for team in lineups:
        for p in team["lineup"]:
            spells = p.get("positions") or []
            if not spells:
                continue  # unused substitute

            minutes_by_position: dict[str, float] = defaultdict(float)
            for spell in spells:
                start = clock_to_minutes(spell["from"])
                end = clock_to_minutes(spell["to"]) if spell.get("to") else match_end
                minutes_by_position[spell["position"]] += max(0.0, end - start)

            minutes = sum(minutes_by_position.values())
            if minutes <= 0:
                continue
            position = max(minutes_by_position, key=minutes_by_position.get)
            rows.append(
                {
                    "match_id": match_id,
                    "team_id": team["team_id"],
                    "team": team["team_name"],
                    "player_id": p["player_id"],
                    # The nickname is the commonly used name ("Alexis Sánchez").
                    "player": p.get("player_nickname") or p["player_name"],
                    "position": position,
                    "position_group": position_group(position),
                    "started": spells[0]["start_reason"] == "Starting XI",
                    "minutes": minutes,
                }
            )
    return pd.DataFrame(rows)
