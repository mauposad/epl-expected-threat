import os
import json
import pandas as pd
from pathlib import Path


def load_json_files_from_folder(folder_path: str) -> list:
    """
    Loads ALL JSON files in a folder and returns a list of parsed objects.
    """
    json_objects = []
    folder = Path(folder_path)

    for json_file in folder.rglob("*.json"):
        with open(json_file, "r", encoding="utf-8") as f:
            try:
                json_objects.append(json.load(f))
            except json.JSONDecodeError:
                print(f"Could not parse {json_file}")

    return json_objects
