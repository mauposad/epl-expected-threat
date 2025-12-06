import pandas as pd
from pathlib import Path

XTHREAT_EVENTS_DIR = Path("statsbomb_pipeline/data/processed/xthreat_events")
OUTPUT = Path("statsbomb_pipeline/data/processed/xthreat_player_match.csv")


def aggregate_player_match_xthreat():
    all_files = list(XTHREAT_EVENTS_DIR.glob("*.parquet"))

    rows = []

    for f in all_files:
        df = pd.read_parquet(f)
        match_id = df["match_id"].iloc[0]

        # Per-player aggregation
        grouped = (
            df.groupby(["player_id", "team_id", "player_name"])
            .agg(
                xThreat_total=("xThreat", "sum"),
                xThreat_pass=(
                    "xThreat",
                    lambda x: x[df.loc[x.index, "event_type"] == "Pass"].sum(),
                ),
                xThreat_carry=(
                    "xThreat",
                    lambda x: x[df.loc[x.index, "event_type"] == "Carry"].sum(),
                ),
                xg_total=("xg", "sum"),
            )
            .reset_index()
        )

        grouped["match_id"] = match_id
        rows.append(grouped)

    final = pd.concat(rows, ignore_index=True)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    final.to_csv(OUTPUT, index=False)

    print(f"✓ Saved player-match xThreat → {OUTPUT}")


if __name__ == "__main__":
    aggregate_player_match_xthreat()
