"""Project-wide constants and file locations.

All paths are anchored to the repository root, so scripts and notebooks work
regardless of the current working directory.
"""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

# StatsBomb Open Data identifiers for the Premier League 2015/16 season.
COMPETITION_ID = 2
SEASON_ID = 27
SEASON_LABEL = "2015/16"

STATSBOMB_BASE_URL = "https://raw.githubusercontent.com/hudl/open-data/master/data"

DATA_DIR = REPO_ROOT / "data"
RAW_DIR = DATA_DIR / "raw" / "statsbomb"
MATCHES_FILE = RAW_DIR / "matches" / str(COMPETITION_ID) / f"{SEASON_ID}.json"
EVENTS_DIR = RAW_DIR / "events"
LINEUPS_DIR = RAW_DIR / "lineups"

PROCESSED_DIR = DATA_DIR / "processed"
MATCHES_TABLE = PROCESSED_DIR / "matches.parquet"
ACTIONS_TABLE = PROCESSED_DIR / "actions.parquet"
XT_GRID_FILE = PROCESSED_DIR / "xt_grid.npy"
PLAYER_MINUTES_TABLE = PROCESSED_DIR / "player_match_minutes.parquet"
PLAYER_MATCH_TABLE = PROCESSED_DIR / "player_match.parquet"
PLAYER_SEASON_TABLE = PROCESSED_DIR / "player_season.parquet"
TEAM_MATCH_TABLE = PROCESSED_DIR / "team_match.parquet"
TEAM_SEASON_TABLE = PROCESSED_DIR / "team_season.parquet"

FIGURES_DIR = REPO_ROOT / "reports" / "figures"
