from dotenv import load_dotenv
import requests
import os

load_dotenv()
API_KEY = os.getenv("HIGHLIGHTLY_API_KEY")
headers = {"x-rapidapi-key": f"{API_KEY}"}


# all ncaa and nfl football teams
r = requests.get("https://american-football.highlightly.net/teams", headers=headers, timeout=15)
print(r.status_code)
# print(r.json())


# get all soccer leagues
r = requests.get("https://soccer.highlightly.net/leagues", headers=headers, timeout=15)
print(r.status_code)
# print(r.json())
