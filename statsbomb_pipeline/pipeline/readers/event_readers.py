import pandas as pd
from pipeline.loaders import load_json_files_from_folder


def load_events(path: str) -> pd.DataFrame:
    data = load_json_files_from_folder(path)

    # Events JSONs are long lists → flatten each
    df = pd.json_normalize([event for match in data for event in match])
    return df
