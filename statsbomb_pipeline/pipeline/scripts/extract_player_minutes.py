import json
import os
import pandas as pd
from pathlib import Path
from tqdm import tqdm

# ----------------------------------------------------
# PATHS
# ----------------------------------------------------
BASE_DIR = Path(__file__).resolve().parents[2]  # statsbomb_pipeline/
RAW_DIR = BASE_DIR / "data" / "raw"
MATCHES_FILE = RAW_DIR / "matches" / "2" / "27.json"  # EPL 2015/2016
LINEUPS_DIR = RAW_DIR / "lineups"
EVENTS_DIR = RAW_DIR / "events"

OUTPUT = BASE_DIR / "data" / "processed" / "player_minutes_2015_2016.parquet"


# ----------------------------------------------------
# LOAD MATCH METADATA
# ----------------------------------------------------
def load_matches():
    with open(MATCHES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


# ----------------------------------------------------
# EXTRACT SUBSTITUTIONS
# ----------------------------------------------------
def extract_sub_events(events_json):
    subs = []
    for ev in events_json:
        if ev.get("type", {}).get("name") == "Substitution":
            minute = ev.get("minute", 0)

            player_off = ev.get("player", {}).get("id")
            player_on = ev.get("substitution", {}).get("replacement", {}).get("id")

            team_id = ev.get("team", {}).get("id")
            team_name = ev.get("team", {}).get("name")

            subs.append(
                {
                    "minute": minute,
                    "off_id": player_off,
                    "on_id": player_on,
                    "team_id": team_id,
                    "team_name": team_name,
                }
            )
    return subs


# ----------------------------------------------------
# PROCESS ONE MATCH
# ----------------------------------------------------
def process_match(match_row):
    match_id = match_row["match_id"]

    home_id = match_row["home_team"]["home_team_id"]
    away_id = match_row["away_team"]["away_team_id"]

    home_name = match_row["home_team"]["home_team_name"]
    away_name = match_row["away_team"]["away_team_name"]

    home_score = match_row["home_score"]
    away_score = match_row["away_score"]

    match_date = match_row.get("match_date", None)

    # Load lineups
    lineup_path = LINEUPS_DIR / f"{match_id}.json"
    if not lineup_path.exists():
        return []

    with open(lineup_path, "r", encoding="utf-8") as f:
        lineups = json.load(f)

    # Load events
    events_path = EVENTS_DIR / f"{match_id}.json"
    if not events_path.exists():
        return []

    with open(events_path, "r", encoding="utf-8") as f:
        events = json.load(f)

    subs = extract_sub_events(events)

    # ----------------------------------------------------
    # SETUP PLAYER REGISTER WITH STARTERS
    # ----------------------------------------------------
    players = {}  # player_id → dict

    for team in lineups:
        team_id = team["team_id"]
        team_name = team["team_name"]

        for p in team["lineup"]:
            pid = p["player_id"]
            pname = p["player_name"]

            # Position: first listed position, per your lineup schema
            pos_list = p.get("positions", [])
            position = pos_list[0]["position"] if pos_list else None

            players[pid] = {
                "match_id": match_id,
                "player_id": pid,
                "player_name": pname,
                "team_id": team_id,
                "team_name": team_name,
                "position": position,
                "is_starter": True,
                "start_min": 0,
                "end_min": 90,
                "home_score": home_score,
                "away_score": away_score,
                "match_date": match_date,
                "opponent_id": away_id if team_id == home_id else home_id,
                "opponent_name": away_name if team_id == home_id else home_name,
            }

    # ----------------------------------------------------
    # PROCESS SUBSTITUTIONS
    # ----------------------------------------------------
    for s in subs:
        minute = s["minute"]
        off_id = s["off_id"]
        on_id = s["on_id"]
        team_id = s["team_id"]
        team_name = s["team_name"]

        # Player OFF
        if off_id in players:
            players[off_id]["end_min"] = minute

        # Player ON
        if on_id is not None:
            if on_id not in players:
                players[on_id] = {
                    "match_id": match_id,
                    "player_id": on_id,
                    "player_name": None,
                    "team_id": team_id,
                    "team_name": team_name,
                    "position": None,
                    "is_starter": False,
                    "start_min": minute,
                    "end_min": 90,
                    "home_score": home_score,
                    "away_score": away_score,
                    "match_date": match_date,
                    "opponent_id": away_id if team_id == home_id else home_id,
                    "opponent_name": away_name if team_id == home_id else home_name,
                }
            else:
                players[on_id]["start_min"] = minute
                players[on_id]["is_starter"] = False

    # Convert to list
    rows = []
    for pid, pdata in players.items():
        minutes = max(0, pdata["end_min"] - pdata["start_min"])
        pdata["minutes_played"] = minutes
        rows.append(pdata)

    return rows


# ----------------------------------------------------
# MAIN EXTRACTION
# ----------------------------------------------------
def run():
    matches = load_matches()
    all_rows = []

    print(f"Processing {len(matches)} matches...\n")

    for m in tqdm(matches):
        rows = process_match(m)
        all_rows.extend(rows)

    df = pd.DataFrame(all_rows)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(OUTPUT, index=False)

    print(f"\nSaved minutes file → {OUTPUT}")
    return df


if __name__ == "__main__":
    run()
