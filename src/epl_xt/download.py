"""Download the StatsBomb Open Data files needed for one competition season.

Fetches the season's match list, then the event and lineup file for every match.
Files that already exist locally are skipped, so the download can be resumed.
"""

import json
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from tqdm import tqdm

from epl_xt import config


def _fetch(url: str, dest: Path, retries: int = 3) -> None:
    if dest.exists():
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".part")
    for attempt in range(1, retries + 1):
        try:
            with urllib.request.urlopen(url, timeout=60) as resp:
                tmp.write_bytes(resp.read())
            tmp.rename(dest)
            return
        except OSError:
            if attempt == retries:
                raise


def download_season(workers: int = 16) -> list[int]:
    """Download matches, events and lineups for the configured season.

    Returns the list of match IDs in the season.
    """
    base = config.STATSBOMB_BASE_URL
    _fetch(
        f"{base}/matches/{config.COMPETITION_ID}/{config.SEASON_ID}.json",
        config.MATCHES_FILE,
    )
    matches = json.loads(config.MATCHES_FILE.read_text(encoding="utf-8"))
    match_ids = sorted(m["match_id"] for m in matches)

    jobs = []
    for match_id in match_ids:
        jobs.append((f"{base}/events/{match_id}.json", config.EVENTS_DIR / f"{match_id}.json"))
        jobs.append((f"{base}/lineups/{match_id}.json", config.LINEUPS_DIR / f"{match_id}.json"))

    pending = [(url, dest) for url, dest in jobs if not dest.exists()]
    if pending:
        with ThreadPoolExecutor(max_workers=workers) as pool:
            futures = [pool.submit(_fetch, url, dest) for url, dest in pending]
            for future in tqdm(as_completed(futures), total=len(futures), desc="Downloading"):
                future.result()

    print(f"{len(match_ids)} matches available under {config.RAW_DIR}")
    return match_ids


if __name__ == "__main__":
    download_season()
