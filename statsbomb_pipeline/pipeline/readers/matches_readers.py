import pandas as pd
from pipeline.loaders import load_json_files_from_folder


def load_matches(path: str) -> pd.DataFrame:
    data = load_json_files_from_folder(path)
    df = pd.json_normalize(data)
    return df
