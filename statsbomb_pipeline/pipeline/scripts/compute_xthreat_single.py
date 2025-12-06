# compute_xthreat_single.py

from pathlib import Path
import pandas as pd
from statsbomb_pipeline.pipeline.xthreat.run_single import compute_xthreat_for_match

# DEFAULT PATHS
MATCH_INDEX = Path("statsbomb_pipeline/data/index/matches.parquet")
OUTPUT_DIR = Path("statsbomb_pipeline/data/processed/xthreat_events")


def run_xthreat_batch():
    """
    Compute event-level xThreat for all matches in the index file.
    Produces one parquet per match at:
        data/processed/xthreat_events/{match_id}.parquet
    """
    df = pd.read_parquet(MATCH_INDEX)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for _, row in df.iterrows():
        match_id = row["match_id"]
        events_path = Path(row["event_path"])
        outpath = OUTPUT_DIR / f"{match_id}.parquet"

        print(f"Processing match {match_id} ...")

        # Event-level xThreat DataFrame
        xt_df = compute_xthreat_for_match(events_path)

        # Attach metadata
        xt_df["match_id"] = match_id
        xt_df["competition_id"] = row["competition_id"]
        xt_df["season_id"] = row["season_id"]
        xt_df["home_team"] = row["home_team"]
        xt_df["away_team"] = row["away_team"]

        xt_df.to_parquet(outpath, index=False)

        print(f"✓ Saved {outpath}")


if __name__ == "__main__":
    run_xthreat_batch()
