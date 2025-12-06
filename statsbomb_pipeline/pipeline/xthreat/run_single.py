# run_single.py
from pathlib import Path
import pandas as pd

from statsbomb_pipeline.pipeline.parsing.events_parser import parse_event_file
from statsbomb_pipeline.pipeline.xthreat.value_iteration import compute_value_table
from statsbomb_pipeline.pipeline.xthreat.xthreat_scorer import score_actions_with_xthreat
from statsbomb_pipeline.pipeline.xthreat.xthreat_aggregator import aggregate_xthreat


# =====================================================
# CONFIGURATION — CHANGE THESE TWO LINES TO TEST ANY MATCH
# =====================================================

EVENTS_PATH = Path("statsbomb_pipeline/data/raw/events/3753972.json")
OUTPUT_DIR = Path("statsbomb_pipeline/data/processed/xthreat_debug")


# =====================================================
# MAIN HELPER FUNCTIONS
# =====================================================


def compute_xthreat_for_match(events_path: Path) -> pd.DataFrame:
    """Return event-level xThreat DataFrame (for batch processor)."""
    parsed_events = parse_event_file(events_path)
    zone_values = compute_value_table(parsed_events)
    scored = score_actions_with_xthreat(parsed_events, zone_values)
    return pd.DataFrame(scored)


def compute_xthreat_and_save(events_path: Path, output_dir: Path):
    """Compute xThreat + save event-level + player-level parquet outputs."""
    match_id = int(events_path.stem)

    parsed_events = parse_event_file(events_path)
    zone_values = compute_value_table(parsed_events)
    scored = score_actions_with_xthreat(parsed_events, zone_values)

    df_events = pd.DataFrame(scored)

    # --- Save event-level xThreat ---
    out_events = output_dir / "xthreat_events"
    out_events.mkdir(parents=True, exist_ok=True)
    df_events.to_parquet(out_events / f"{match_id}.parquet", index=False)

    # --- Aggregate per player ---
    agg = aggregate_xthreat(scored)
    df_players = pd.DataFrame(
        {
            "match_id": match_id,
            "player_name": list(agg["player_xT"].keys()),
            "xThreat": list(agg["player_xT"].values()),
        }
    )

    out_players = output_dir / "xthreat_player"
    out_players.mkdir(parents=True, exist_ok=True)
    df_players.to_parquet(out_players / f"{match_id}.parquet", index=False)

    print(f"✓ Finished match {match_id}")
    print(f"✓ Events saved to:   {out_events / f'{match_id}.parquet'}")
    print(f"✓ Player xT saved to: {out_players / f'{match_id}.parquet'}")


# =====================================================
# SCRIPT EXECUTION ENTRYPOINT
# =====================================================

if __name__ == "__main__":
    compute_xthreat_and_save(EVENTS_PATH, OUTPUT_DIR)
