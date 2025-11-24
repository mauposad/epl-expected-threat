from pathlib import Path
import json
import pandas as pd


def build_match_index(matches_root: Path, events_root: Path, output: Path):
    rows = []

    # Loop over competition folders (e.g. 2, 7, 44, 49...)
    for competition_dir in matches_root.iterdir():
        if not competition_dir.is_dir():
            continue

        competition_id = int(competition_dir.name)

        # Loop over season files inside each competition folder
        for season_file in competition_dir.glob("*.json"):
            season_id = int(season_file.stem)

            # Load season's matches list
            matches = json.loads(season_file.read_text(encoding="utf-8"))

            for match in matches:
                match_id = match["match_id"]

                home_team = match["home_team"]["home_team_name"]
                away_team = match["away_team"]["away_team_name"]

                event_path = events_root / f"{match_id}.json"

                rows.append(
                    {
                        "match_id": match_id,
                        "competition_id": competition_id,
                        "season_id": season_id,
                        "home_team": home_team,
                        "away_team": away_team,
                        "event_path": str(event_path),
                    }
                )

    df = pd.DataFrame(rows)
    output.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(output, index=False)
    print(f"Match index saved to: {output}")


if __name__ == "__main__":
    repo_root = Path("statsbomb_pipeline")

    matches_root = repo_root / "data/raw/matches"
    events_root = repo_root / "data/raw/events"
    output = repo_root / "data/index/matches.parquet"

    build_match_index(matches_root, events_root, output)
