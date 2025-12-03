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
EVENTS_DIR = RAW_DIR / "events"  # only used if we want match_length from events

OUTPUT = BASE_DIR / "data" / "processed" / "player_minutes_2015_2016.csv"

DEFAULT_MATCH_LENGTH = 90.0


# ----------------------------------------------------
# UTIL: PARSE "MM:SS" TO FLOAT MINUTES
# ----------------------------------------------------
def parse_time_str(t):
    """
    Convert 'MM:SS' string to float minutes.
    If t is None → treat as end of match.
    """
    if t is None:
        return DEFAULT_MATCH_LENGTH
    try:
        mm, ss = t.split(":")
        return int(mm) + int(ss) / 60.0
    except:
        return 0.0


# ----------------------------------------------------
# LOAD MATCH METADATA
# ----------------------------------------------------
def load_matches():
    with open(MATCHES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


# ----------------------------------------------------
# GET MATCH LENGTH (OPTIONAL)
# ----------------------------------------------------
def get_match_length(events_json):
    """
    Optional: find actual max minute from events.
    If events are missing or bad, fallback to 90.0.
    """
    try:
        max_minute = max(ev.get("minute", 0) for ev in events_json)
        return max(max_minute, 90.0)
    except:
        return 90.0


# ----------------------------------------------------
# PROCESS ONE MATCH USING ONLY LINEUPS FOR MINUTES
# ----------------------------------------------------
def process_match(match_row):
    match_id = match_row["match_id"]

    home_id = match_row["home_team"]["home_team_id"]
    away_id = match_row["away_team"]["away_team_id"]

    home_name = match_row["home_team"]["home_team_name"]
    away_name = match_row["away_team"]["away_team_name"]

    home_score = match_row["home_score"]
    away_score = match_row["away_score"]
    match_date = match_row.get("match_date")

    # Load lineups
    lineup_path = LINEUPS_DIR / f"{match_id}.json"
    if not lineup_path.exists():
        return []

    with open(lineup_path, "r", encoding="utf-8") as f:
        lineups = json.load(f)

    # Load events only to compute match_length — not for subs
    events_path = EVENTS_DIR / f"{match_id}.json"
    if events_path.exists():
        with open(events_path, "r", encoding="utf-8") as f:
            events = json.load(f)
        match_length = get_match_length(events)
    else:
        match_length = DEFAULT_MATCH_LENGTH

    rows = []

    # ----------------------------------------------------
    # TRUE MINUTES + STARTER + POSITION LOGIC
    # ----------------------------------------------------
    for team in lineups:
        team_id = team["team_id"]
        team_name = team["team_name"]

        opponent_id = away_id if team_id == home_id else home_id
        opponent_name = away_name if team_id == home_id else home_name

        for p in team["lineup"]:
            pid = p["player_id"]
            pname = p["player_name"]
            spells = p.get("positions", [])

            # Compute minutes from spells
            if not spells:
                minutes_played = 0.0
                position_name = None
                start_min = None
                end_min = None
                is_starter = False
            else:
                minutes_played = 0.0
                start_min = float("inf")
                end_min = 0.0

                # POSITION = first spell's position (standard StatsBomb convention)
                position_name = spells[0].get("position")

                # Check each time spell
                for sp in spells:
                    t_from = parse_time_str(sp.get("from"))
                    t_to = parse_time_str(sp.get("to"))

                    # Update minutes
                    minutes_played += max(0.0, t_to - t_from)

                    # Update start/end min ranges
                    start_min = min(start_min, t_from)
                    end_min = max(end_min, t_to)

                # Starter = any spell starts at 0:00
                is_starter = any(parse_time_str(sp.get("from")) == 0.0 for sp in spells)

                # Normalize infinite values if spells were malformed
                if start_min == float("inf"):
                    start_min = None

            rows.append(
                {
                    "match_id": match_id,
                    "player_id": pid,
                    "player_name": pname,
                    "team_id": team_id,
                    "team_name": team_name,
                    "position": position_name,
                    "is_starter": is_starter,
                    "start_min": start_min,
                    "end_min": end_min,
                    "minutes_played": minutes_played,
                    "home_score": home_score,
                    "away_score": away_score,
                    "match_date": match_date,
                    "opponent_id": opponent_id,
                    "opponent_name": opponent_name,
                }
            )

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
    df.to_csv(OUTPUT, index=False)

    print(f"\nSaved minutes file → {OUTPUT}")
    return df


if __name__ == "__main__":
    run()
