"""Playing around with the API Service FootyStats
Just using the basic endpoints to see what kind of data I am working with"""

from dotenv import load_dotenv
import requests
import os
import json, jmespath
import pandas as pd
import ast
from apis.data_utils import fetch_season_data, load_team_stats, clean_team_stats

load_dotenv()
FOOTYSTATS_API_KEY = os.getenv("FOOTYSTATS_API_KEY")

season_id = 12325
data = fetch_season_data(season_id, True)

if data:
    print(f"Got {len(data['data'])} teams")
else:
    print("Failed to fetch data. Check logs.")

df = load_team_stats(data)
df_clean = clean_team_stats(df, True, True)
df_full_numeric = clean_team_stats(df, keep_overall=False)
print(df_clean.shape)
print(df_full_numeric.head)


df_clean.to_parquet("data/processed/season_12325_clean.parquet")

# can read in any time with
# df_clean.to_parquet("data/processed/season_12325_clean.parquet")


# 15050 (2025-2026) & 12325 (2024-2025)
