import pandas as pd


df = pd.read_parquet("statsbomb_pipeline/data/processed/team/team_match.parquet")
print(df.head())
print(df.shape)


# 1. Goals per match sanity
print(df.groupby("match_id")["goals"].sum().describe())

print(df["outcome"].value_counts())

print(df[["goals", "team_xg"]].corr())
