from pathlib import Path
import pandas as pd

from statsbomb_pipeline.pipeline.parsing.events_parser import parse_event_file
from statsbomb_pipeline.pipeline.xthreat.value_iteration import test_value_iteration


def compute_xthreat_for_match(events_path: Path) -> pd.DataFrame:
    parsed = parse_event_file(events_path)
    xt = test_value_iteration(parsed)

    if not isinstance(xt, pd.DataFrame):
        xt = pd.DataFrame(xt)

    return xt
