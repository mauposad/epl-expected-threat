from pathlib import Path
import pandas as pd


# Paths
MATCH_INDEX = Path("statsbomb_pipeline/data/index/matches.parquet")
XTHREAT_DIR = Path("statsbomb_pipeline/data/processed/xthreat_events")
OUTPUT_PATH = Path("statsbomb_pipeline/data/processed/xthreat/xthreat_events.parquet")

# EPL 2015/2016
TARGET_COMPETITION_ID = 2
TARGET_SEASON_ID = 27


def combine_xthreat_events():
    """
    Combine xThreat event parquets ONLY for Premier League 2015/2016.
    Produces a clean event-level dataset ready for team-level aggregation.
    """
    # Load index
    df_index = pd.read_parquet(MATCH_INDEX)

    # Filter to EPL 2015/16
    filtered = df_index[
        (df_index["competition_id"] == TARGET_COMPETITION_ID)
        & (df_index["season_id"] == TARGET_SEASON_ID)
    ].copy()

    valid_match_ids = set(filtered["match_id"].astype(int).tolist())

    print(f"Found {len(valid_match_ids)} matches for EPL 2015/2016.")
    print("Combining only these xThreat event files...")

    all_rows = []

    for match_id in valid_match_ids:
        fpath = XTHREAT_DIR / f"{match_id}.parquet"
        if not fpath.exists():
            print(f"WARNING: Missing xThreat file for match_id {match_id}")
            continue

        df = pd.read_parquet(fpath)
        all_rows.append(df)

    # Combine matches into one dataframe
    full_df = pd.concat(all_rows, ignore_index=True)

    # Save outputs
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    full_df.to_parquet(OUTPUT_PATH, index=False)
    full_df.to_csv(OUTPUT_PATH.with_suffix(".csv"), index=False)

    print("\nSaved combined EPL 2015/2016 xThreat event dataframe to:")
    print(f"  {OUTPUT_PATH}")
    print(f"  {OUTPUT_PATH.with_suffix('.csv')}")
    print(f"Total rows: {len(full_df):,}")

    return full_df


if __name__ == "__main__":
    combine_xthreat_events()
