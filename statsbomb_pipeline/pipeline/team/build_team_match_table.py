from pathlib import Path
import pandas as pd

from statsbomb_pipeline.pipeline.team.team_match_aggregator import (
    add_event_flags,
    aggregate_team_match,
)

# Paths
XTHREAT_EVENTS = Path("statsbomb_pipeline/data/processed/xthreat/xthreat_events.parquet")
OUTPUT_DIR = Path("statsbomb_pipeline/data/processed/team")


def build_team_match_table():
    """
    Full end-to-end creation of the team-level match table
    from event-level xThreat enhanced event data.
    """
    print("Loading combined xThreat event dataframe...")
    events = pd.read_parquet(XTHREAT_EVENTS)
    print(f"Loaded {len(events):,} event rows.")

    # Add flags for shots, passes, carries, PPAs, etc.
    print("Adding event-level flags...")
    flagged = add_event_flags(events)

    # Aggregate into team-match level table
    print("Aggregating into team-match table...")
    team_match = aggregate_team_match(flagged)

    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    out_parquet = OUTPUT_DIR / "team_match.parquet"
    out_csv = OUTPUT_DIR / "team_match.csv"

    team_match.to_parquet(out_parquet, index=False)
    team_match.to_csv(out_csv, index=False)

    print("Saved team match table:")
    print(f"  {out_parquet}")
    print(f"  {out_csv}")

    return team_match


if __name__ == "__main__":
    build_team_match_table()
