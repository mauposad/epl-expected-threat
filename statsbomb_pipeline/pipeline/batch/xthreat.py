from pathlib import Path
import pandas as pd

from statsbomb_pipeline.pipeline.xthreat.run_single import compute_xthreat_for_match


def run_xthreat_batch(
    index_path: Path,
    output_dir: Path,
    competition_ids=None,
    season_ids=None,
    match_ids=None,
):
    df = pd.read_parquet(index_path)

    if competition_ids is not None:
        df = df[df["competition_id"].isin(competition_ids)]
    if season_ids is not None:
        df = df[df["season_id"].isin(season_ids)]
    if match_ids is not None:
        df = df[df["match_id"].isin(match_ids)]

    output_dir.mkdir(parents=True, exist_ok=True)

    for _, row in df.iterrows():
        match_id = row["match_id"]

        print(f"Processing match {match_id}…")

        events_path = Path(row["event_path"])

        if not events_path.exists():
            print(f"  ⚠️  Event file missing: {events_path}")
            continue

        xt_df = compute_xthreat_for_match(events_path)

        xt_df["match_id"] = match_id
        xt_df["competition_id"] = row["competition_id"]
        xt_df["season_id"] = row["season_id"]
        xt_df["home_team"] = row["home_team"]
        xt_df["away_team"] = row["away_team"]

        outpath = output_dir / f"{match_id}.parquet"
        xt_df.to_parquet(outpath, index=False)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Batch xThreat processing")
    parser.add_argument(
        "--index",
        type=Path,
        default=Path("statsbomb_pipeline/data/index/matches.parquet"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("statsbomb_pipeline/data/processed/xthreat"),
    )
    parser.add_argument("--competition", type=int, nargs="*")
    parser.add_argument("--season", type=int, nargs="*")
    parser.add_argument("--match", type=int, nargs="*")

    args = parser.parse_args()

    run_xthreat_batch(
        index_path=args.index,
        output_dir=args.output,
        competition_ids=args.competition,
        season_ids=args.season,
        match_ids=args.match,
    )
