import pandas as pd
import re
from typing import List, Dict, Set
from MetricGrouper import MetricGrouper

# ============================================================================
# USAGE EXAMPLE WITH YOUR DATA
# ============================================================================

# Load your data
df = pd.read_csv("../../data_pipeline/data/cleaned/premier_league_cleaned.csv")
grouper = MetricGrouper(df)

print("=" * 80)
print("FLEXIBLE METRIC EXTRACTION SYSTEM")
print("=" * 80)
print(f"\nTotal columns in dataset: {len(df.columns)}")
print(f"Total teams: {len(df)}\n")

# ============================================================================
# DEFINE YOUR METRIC GROUPS WITH FLEXIBLE KEYWORD MATCHING
# ============================================================================

metric_groups = {
    "scoring": {"keywords": ["goal", "scored", "xg"], "exclude": ["conceded", "against", "prevented", "kicks"]},
    "defensive": {
        "keywords": ["conceded", "against", "clean", "sheets", "defense", "defensive"],
        "exclude": ["for", "team"],
    },
    "shots": {"keywords": ["shot", "shots"], "exclude": []},
    "possession": {"keywords": ["possession", "pass"], "exclude": []},
    "corners": {"keywords": ["corner"], "exclude": []},
    "cards_discipline": {"keywords": ["card", "cards", "foul"], "exclude": []},
    "set_pieces": {"keywords": ["freekick", "penalty", "penalties"], "exclude": []},
    "match_outcomes": {"keywords": ["win", "draw", "loss", "points", "position"], "exclude": []},
    "halftime": {"keywords": ["ht_", "_ht", "half", "1h", "2h", "fh"], "exclude": []},
    "offsides": {"keywords": ["offside"], "exclude": []},
    "attacks": {"keywords": ["attack"], "exclude": []},
    "throwins": {"keywords": ["throwin"], "exclude": []},
    "goal_kicks": {"keywords": ["goal_kick"], "exclude": []},
}

# ============================================================================
# PREVIEW EACH GROUP
# ============================================================================

print("METRIC GROUP PREVIEWS")
print("=" * 80)

for group_name, config in metric_groups.items():
    preview = grouper.preview_group(group_name, config["keywords"], config["exclude"], limit=3)

    print(f"\n📊 {group_name.upper()}")
    print(f"   Found {preview['num_columns']} columns")
    print(f"   Columns: {', '.join(preview['columns'][:5])}")
    if len(preview["columns"]) > 5:
        print(f"            ... and {len(preview['columns']) - 5} more")
    print()

# ============================================================================
# EXTRACT SPECIFIC GROUPS FOR ANALYSIS
# ============================================================================

print("\n" + "=" * 80)
print("EXTRACTING METRIC SUBSETS FOR ANALYSIS")
print("=" * 80)

# Extract scoring metrics
scoring_df = grouper.get_metric_subset(
    "scoring", metric_groups["scoring"]["keywords"], metric_groups["scoring"]["exclude"]
)

print(f"\n✅ Scoring metrics extracted: {scoring_df.shape[1] - 1} columns")
print(f"   Shape: {scoring_df.shape}")
print(f"   Sample columns: {list(scoring_df.columns[1:6])}")

# Extract defensive metrics
defensive_df = grouper.get_metric_subset(
    "defensive", metric_groups["defensive"]["keywords"], metric_groups["defensive"]["exclude"]
)

print(f"\n✅ Defensive metrics extracted: {defensive_df.shape[1] - 1} columns")
print(f"   Shape: {defensive_df.shape}")

# Extract corners
corners_df = grouper.get_metric_subset(
    "corners", metric_groups["corners"]["keywords"], metric_groups["corners"]["exclude"]
)

print(f"\n✅ Corner metrics extracted: {corners_df.shape[1] - 1} columns")
print(f"   Shape: {corners_df.shape}")

print("\n" + "=" * 80)
print("QUICK ANALYSIS EXAMPLE - Top 5 Scoring Teams")
print("=" * 80)

# Example analysis on scoring subset
if "seasonGoals_overall" in scoring_df.columns:
    top_scorers = scoring_df.nlargest(5, "seasonGoals_overall")[["name", "seasonGoals_overall", "xg_for_avg_overall"]]
    print("\n", top_scorers.to_string(index=False))

print("\n" + "=" * 80)
print("✅ System ready! Use grouper.get_metric_subset() to extract any group")
print("=" * 80)
