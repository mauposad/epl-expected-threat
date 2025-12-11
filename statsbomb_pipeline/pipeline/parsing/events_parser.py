import json
from pathlib import Path


def parse_event_file(path: str | Path):
    """
    Parse a single StatsBomb event file and extract only
    Pass, Carry, and Shot events for xThreat calculations.
    """
    path = Path(path)
    match_id = int(path.stem)  # filename without extension
    with path.open("r", encoding="utf-8") as f:
        events = json.load(f)

    parsed = []

    for e in events:
        etype = e.get("type", {}).get("name")
        loc = e.get("location")

        # Base row for all extracted events
        row = {
            "match_id": match_id,
            "event_type": etype,
            "team_id": e.get("team", {}).get("id"),
            "team": e.get("team", {}).get("name"),
            "player_id": e.get("player", {}).get("id"),
            "player_name": e.get("player", {}).get("name"),
            "possession": e.get("possession"),
            "timestamp": e.get("timestamp"),
            "minute": e.get("minute"),
            "second": e.get("second"),
            "x": loc[0] if loc else None,
            "y": loc[1] if loc else None,
        }

        # Extract PASS info
        if etype == "Pass":
            p = e.get("pass", {})
            end = p.get("end_location")
            row["end_x"] = end[0] if end else None
            row["end_y"] = end[1] if end else None
            row["outcome"] = p.get("outcome", {}).get("name")
            parsed.append(row)
            continue

        # Extract CARRY info
        if etype == "Carry":
            c = e.get("carry", {})
            end = c.get("end_location")
            row["end_x"] = end[0] if end else None
            row["end_y"] = end[1] if end else None
            parsed.append(row)
            continue

        # Extract SHOT info (need xG for reward)
        if etype == "Shot":
            s = e.get("shot", {})
            row["xg"] = s.get("statsbomb_xg")
            row["outcome"] = s.get("outcome", {}).get("name")
            parsed.append(row)
            continue

        # Ignore everything else (Fouls, Starting XI, Block, etc)

    return parsed
