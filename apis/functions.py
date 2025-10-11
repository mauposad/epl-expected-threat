from dotenv import load_dotenv
import requests
import os
import json, jmespath
import pandas as pd

"""
Helper functions for the footystats api
These functions will help build the data pipeline
"""

load_dotenv()
FOOTYSTATS_API_KEY = os.getenv("FOOTYSTATS_API_KEY")


def get_previous_teams():
    """
    What do we expect our functions to be returning?
    Just how much processing will we be doing within our helper functions?
    # 15050 (2025-2026) & 12325 (2024-2025)
    Needs to be hard coded for now. Not sure how to use dynamically since
    only certain calls work
    """
    r = requests.get(
        f"https://api.football-data-api.com/league-teams?key={FOOTYSTATS_API_KEY}&season_id=12325&include=stats "
    )


def get_team_stats(team_id: int):  # 59 for arsenal but will need to be passing this in
    r = requests.get(f"https://api.football-data-api.com/team?key={FOOTYSTATS_API_KEY}&team_id={team_id}&include=stats")


def get_todays_matches():  # Need to revise further
    r = requests.get(f"https://api.football-data-api.com/todays-matches?key={FOOTYSTATS_API_KEY}")
