"""
Docstring for statsbomb_pipeline.script
Sanity checks for the extract_palyer_minutes.py file.
"""

import pandas as pd

# df = pd.read_csv("data/processed/player_minutes_2015_2016.csv")
# print(df.head(20))
# print(df.columns)
# print(df.shape)

# players with 90+ minutes but zero events later (after we wire that in),
# but for now, just look at multiple keepers with full 90 for the same team/match
# suspicious = (
#     df[df["minutes_played"] >= 90]
#     .groupby(["match_id", "team_id"])
#     .size()
#     .reset_index(name="players_90_plus")
# )

# suspicious = suspicious[suspicious["players_90_plus"] > 11]
# print(suspicious.head(10))
# team_minutes = (
#     df.groupby(["match_id", "team_id"])["minutes_played"]
#     .sum()
#     .reset_index(name="total_minutes")
# )
# print(team_minutes["total_minutes"].describe())
# print(team_minutes.sort_values("total_minutes").head())
# print(team_minutes.sort_values("total_minutes").tail())


# active_players = (
#     df[df["minutes_played"] > 0]
#     .groupby(["match_id", "team_id"])
#     .size()
#     .reset_index(name="players_with_minutes")
# )
# print(active_players["players_with_minutes"].describe())
# print(active_players.sort_values("players_with_minutes").head())
# print(active_players.sort_values("players_with_minutes").tail())

df = pd.read_parquet("data/processed/xthreat/3753972.parquet")
print(df.head(20))
print(df.columns)
