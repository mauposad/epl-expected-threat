"""Playing around with the API Service FootyStats
Just using the basic endpoints to see what kind of data I am working with"""

from dotenv import load_dotenv
from fastapi import FastAPI
import requests
import os
import json, jmespath
import pandas as pd
import ast


load_dotenv()
FOOTYSTATS_API_KEY = os.getenv("FOOTYSTATS_API_KEY")

# get a list of all leagues
# r = requests.get(f"https://api.football-data-api.com/league-list?key={FOOTYSTATS_API_KEY}")
# print(r)
# print(r.status_code)
# print(r.json())

# Get a list of todays matches
# r = requests.get(f"https://api.football-data-api.com/todays-matches?key={FOOTYSTATS_API_KEY}")
# print(r.status_code)
# print(r.json())

# r = requests.get(f"https://api.football-data-api.com/league-list?key={FOOTYSTATS_API_KEY}")
# r.raise_for_status()
# data = r.json()

# 15050 (2025-2026) & 12325 (2024-2025)

r = requests.get(f"https://api.football-data-api.com/league-list?key={FOOTYSTATS_API_KEY}")
r.raise_for_status()
data = r.json()
with open("payload.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"Saved payload.json with ", len(json.dumps(data)), "characters")

with open("payload.json") as f:
    subset = json.load(f)

# Getting Arsenal teams stats (team_id = 59)
# r = requests.get(f"https://api.football-data-api.com/team?key={FOOTYSTATS_API_KEY}&team_id=60&include=stats")
# r.raise_for_status()
# # print(r.json())
# data = r.json()

# # shouldn't be so hard coded, find a more dynamic way of doing things
# expr = "data[0:2]"  # can do 0:n to pull different amounts of packages.
# subset = jmespath.search(expr, data)

# # Serializing back to file
# with open("payload.json", "w", encoding="utf-8") as f:
#     json.dump(subset, f, indent=2, ensure_ascii=False)

# # always re-serialize api's to enforce validity
# print("Saved payload.json with", len(json.dumps(subset)), "characters")


# with open("payload.json") as f:
#     subset = json.load(f)


# df = pd.json_normalize(subset, sep="_", max_level=None)
# print(df.shape)
# print(df.columns[:25])

# print(df.at[1, "stats_additional_info_dangerous_attacks_num_away"])
