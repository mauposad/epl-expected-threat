"""Playing around with the API Service FootyStats
Just using the basic endpoints to see what kind of data I am working with"""

from dotenv import load_dotenv
from fastapi import FastAPI
import requests
import os


load_dotenv()
FOOTYSTATS_API_KEY = os.getenv("FOOTYSTATS_API_KEY")

# get a list of all leagues
r = requests.get(f"https://api.football-data-api.com/league-list?key={FOOTYSTATS_API_KEY}")
# print(r)
print(r.status_code)
# print(r.json())

# Get a list of todays matches
r = requests.get(f"https://api.football-data-api.com/todays-matches?key={FOOTYSTATS_API_KEY}")
print(r.status_code)
# print(r.json())

# Getting each teams stats
r = requests.get(f"https://api.football-data-api.com/team?key={FOOTYSTATS_API_KEY}&team_id=59&include=stats")
print(r.status_code)
print(r.json())


"""Notes:

Formatting from said API Service could prove to be very difficult. Automation on its own will be a challenge in itself. """
