from dotenv import load_dotenv
import requests
import os
import json, jmespath
import pandas as pd
import logging
from pathlib import Path

"""
Helper functions for the footystats api
These functions will help build the data pipeline
# 15050 (2025 - 2026) 12325 (2024 - 2025)
"""
logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
FOOTYSTATS_BASE_URL = "https://api.football-data-api.com/league-teams"

load_dotenv()
FOOTYSTATS_API_KEY = os.getenv("FOOTYSTATS_API_KEY")


def fetch_season_data(season_id: int, save_to_file: bool = True, output_dir: str = "data", timeout: int = 30):
    """
    Fetches team and stats data for a given season from the FootyStats API and saves it to a file.
    League Teams API Call

    Args:
        season_id (int): The season ID to fetch data for.
        save_to_file (bool): Whether to save the data to a JSON file (default: True).
        output_dir (str): Directory where the JSON file will be stored (default: "data").
        timeout (int): Timeout in seconds for the API request (default: 30).

    Returns:
        dict: Parsed JSON response if successful, else None.
    """
    global FOOTYSTATS_API_KEY
    url = f"{FOOTYSTATS_BASE_URL}?key={FOOTYSTATS_API_KEY}&season_id={season_id}&include=stats"
    try:
        logging.info(f"Fetching data for season_id={season_id}...")
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        data = response.json()

        if not data or "data" not in data or not isinstance(data["data"], list):
            logging.warning(f"Invalid or empty data structure for season_id={season_id}")
            return None

        logging.info(f"Successfully retrieved {len(data['data'])} teams for season_id={season_id}")

        # Save data to file if requested
        if save_to_file:
            Path(output_dir).mkdir(parents=True, exist_ok=True)
            output_file = Path(output_dir) / f"season_{season_id}.json"
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            logging.info(f"Data saved to {output_file.resolve()}")

        return data

    except requests.exceptions.Timeout:
        logging.error(f"Request timed out after {timeout}s for season_id={season_id}")
    except requests.exceptions.HTTPError as e:
        logging.error(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")
    except ValueError as e:
        logging.error(f"Failed to parse JSON: {e}")

    return None


def load_team_stats(json_data: dict) -> pd.DataFrame:
    """
    Takes a JSON package from FootyStats API and converts it into
    a DataFrame with team names as rows and team stats as columns.

    Args:
        json_data (dict): The parsed JSON object (not a file).

    Returns:
        pd.DataFrame: DataFrame with team names as index and stats as columns.
    """
    # Extract the list of teams
    teams = json_data.get("data", [])
    if not teams:
        raise ValueError("No team data found in provided JSON package.")

    # Extract team names
    team_names = pd.DataFrame([{"name": t["name"]} for t in teams])

    # Flatten the nested stats dict
    stats_df = pd.json_normalize([t["stats"] for t in teams])

    # Concatenate team names with their stats
    df = pd.concat([team_names, stats_df], axis=1)

    # Set team name as index
    df.set_index("name", inplace=True)

    return df


import pandas as pd


def clean_team_stats(df: pd.DataFrame, keep_overall: bool = True, drop_non_numeric: bool = True) -> pd.DataFrame:
    """
    Cleans the team stats DataFrame by filtering columns and dropping unwanted data types.

    Args:
        df (pd.DataFrame): The raw team stats DataFrame.
        keep_overall (bool): If True, keep only columns that end with '_overall' (default: True).
        drop_non_numeric (bool): If True, drop columns that contain non-numeric values (default: True).

    Returns:
        pd.DataFrame: A cleaned DataFrame ready for analysis.
    """
    cleaned_df = df.copy()

    if keep_overall:
        cleaned_df = cleaned_df[[col for col in cleaned_df.columns if col.endswith("_overall")]]

    if drop_non_numeric:
        cleaned_df = cleaned_df.select_dtypes(include=["number"])

    return cleaned_df


def get_team_stats(team_id: int):  # 59 for arsenal but will need to be passing this in ( will be used for current year)
    r = requests.get(f"https://api.football-data-api.com/team?key={FOOTYSTATS_API_KEY}&team_id={team_id}&include=stats")


def get_todays_matches():  # Need to revise further
    r = requests.get(f"https://api.football-data-api.com/todays-matches?key={FOOTYSTATS_API_KEY}")
