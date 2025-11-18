import pandas as pd
from pipeline.loaders import load_json_files_from_folder


def load_three_sixty(path: str) -> pd.DataFrame:
    data = load_json_files_from_folder(path)

    # these files are lists of event-level freeze frame data
    df = pd.json_normalize(data)
    return df
