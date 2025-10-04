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

# Getting Arsenal teams stats (team_id = 59)
r = requests.get(f"https://api.football-data-api.com/team?key={FOOTYSTATS_API_KEY}&team_id=59&include=stats")
r.raise_for_status()
# print(r.json())
data = r.json()

expr = "data[0]"
subset = jmespath.search(expr, data)

# Serializing back to file
with open("payload.json", "w", encoding="utf-8") as f:
    json.dump(subset, f, indent=2, ensure_ascii=False)
# always re-serialize api's to enforce validity

print("Saved payload.json with", len(json.dumps(subset)), "characters")


with open("payload.json") as f:
    data = json.load(f)


# Still have a nested package within my dataframe


df = pd.json_normalize(subset, max_level=None)
print(df.shape)
print(df.head)
print(df.tail)
print(df.columns.tolist)


pd.set_option("display.max_rows", 15)  # show all rows
pd.set_option("display.max_columns", None)  # show all columns
pd.set_option("display.width", None)  # don't wrap lines
pd.set_option("display.colheader_justify", "center")  # headers aligned
pd.set_option("display.precision", 3)  # decimals precision

print(df)
