from pipeline.readers.event_readers import load_events
from pipeline.readers.lineups_readers import load_lineups
from pipeline.readers.matches_readers import load_matches
from pipeline.readers.three_sixty_readers import load_three_sixty
from pipeline.readers.competitions_readers import load_competitions


def load_statsbomb_dataset(base_path: str):
    return {
        "events": load_events(f"{base_path}/events"),
        "lineups": load_lineups(f"{base_path}/lineups"),
        "matches": load_matches(f"{base_path}/matches"),
        "three_sixty": load_three_sixty(f"{base_path}/three-sixty"),
        "competitions": load_competitions(f"{base_path}/competitions.json"),
    }
