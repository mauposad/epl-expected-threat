"""End-to-end pipeline: raw StatsBomb JSON -> xT model -> modelling tables.

Run from anywhere with:

    python -m epl_xt.pipeline            # download (if needed) and build everything
    python -m epl_xt.pipeline --no-download
"""

import argparse
import json
from concurrent.futures import ProcessPoolExecutor

import numpy as np
import pandas as pd

from epl_xt import config
from epl_xt.download import download_season
from epl_xt.events import parse_events
from epl_xt.minutes import match_end_minute, player_minutes
from epl_xt.tables import (
    add_action_metrics,
    build_matches_table,
    build_player_match_table,
    build_player_season_table,
    build_team_match_table,
    build_team_season_table,
)
from epl_xt.xthreat import ExpectedThreat


def _load_match(match_id: int) -> tuple[pd.DataFrame, pd.DataFrame]:
    events_path = config.EVENTS_DIR / f"{match_id}.json"
    actions = parse_events(events_path)
    end = match_end_minute(json.loads(events_path.read_text(encoding="utf-8")))
    minutes = player_minutes(config.LINEUPS_DIR / f"{match_id}.json", end)
    return actions, minutes


def fit_xt_model(actions: pd.DataFrame) -> ExpectedThreat:
    """Fit xT on open-play actions only (no penalties or set-piece restarts)."""
    return ExpectedThreat().fit(actions[~actions["set_piece"]])


def run(download: bool = True) -> None:
    if download:
        download_season()

    matches = build_matches_table(config.MATCHES_FILE)
    print(f"Parsing {len(matches)} matches...")
    with ProcessPoolExecutor() as pool:
        results = list(pool.map(_load_match, matches["match_id"], chunksize=8))
    actions = pd.concat([r[0] for r in results], ignore_index=True)
    minutes = pd.concat([r[1] for r in results], ignore_index=True)
    print(f"  {len(actions):,} passes, carries and shots")

    model = fit_xt_model(actions)
    print(
        f"Fitted xT on the full season ({model.n_iter_} iterations, max zone value {model.values_.max():.3f})"
    )
    # Set-piece restarts are not credited with xT; the model describes open play.
    actions["xt"] = np.where(actions["set_piece"], 0.0, model.rate(actions))
    actions = add_action_metrics(actions)

    player_match = build_player_match_table(actions, minutes)
    team_match = build_team_match_table(actions, matches)
    outputs = {
        config.MATCHES_TABLE: matches,
        config.ACTIONS_TABLE: actions,
        config.PLAYER_MINUTES_TABLE: minutes,
        config.PLAYER_MATCH_TABLE: player_match,
        config.PLAYER_SEASON_TABLE: build_player_season_table(player_match),
        config.TEAM_MATCH_TABLE: team_match,
        config.TEAM_SEASON_TABLE: build_team_season_table(team_match),
    }

    config.PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    np.save(config.XT_GRID_FILE, model.grid)
    for path, df in outputs.items():
        df.to_parquet(path, index=False)
        print(f"  wrote {path.relative_to(config.REPO_ROOT)} ({len(df):,} rows)")


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--no-download", action="store_true", help="use raw data already on disk")
    args = parser.parse_args()
    run(download=not args.no_download)


if __name__ == "__main__":
    main()
