import pandas as pd
import numpy as np
from typing import List, Dict, Set
from metric_grouper import MetricGrouper
import warnings

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


# Extract ALL metric subsets into a dictionary
metric_subsets = {}

for group_name, config in metric_groups.items():
    subset_df = grouper.get_metric_subset(group_name, config["keywords"], config["exclude"])
    metric_subsets[group_name] = subset_df
    print(f"✅ {group_name}: {subset_df.shape[1] - 1} columns, {subset_df.shape[0]} rows")

# Now you can access any subset like:
# metric_subsets['scoring']
# metric_subsets['defensive']
# metric_subsets['corners']
# etc.

# To see all available groups:
print("\nAvailable metric groups:")
for group in metric_subsets.keys():
    print(f"  - {group}")


import numpy as np
import warnings

warnings.filterwarnings("ignore")

print("=" * 80)
print("CORRELATION WITH WINNING METRICS - FINDING THE WINNING FORMULA (CORRECTED)")
print("=" * 80)

# Define winning indicators (target variables)
winning_metrics = ["points", "winPercentage_overall", "leaguePosition_overall"]

# Check which winning metrics exist in the original dataframe
available_targets = [m for m in winning_metrics if m in df.columns]

if not available_targets:
    print("⚠️  No winning metrics found! Looking for: points, winPercentage_overall, leaguePosition_overall")
else:
    print(f"\n🎯 Target Variables: {', '.join(available_targets)}")
    print("Note: leaguePosition is INVERSE (lower = better)")
    print("Note: Excluding cross-correlations between target variables\n")

# Store correlations with winning
winning_correlations = {}

for group_name, subset_df in metric_subsets.items():
    print(f"\n{'=' * 80}")
    print(f"📊 {group_name.upper()} METRICS vs WINNING")
    print(f"{'=' * 80}")

    # Merge with winning metrics from original df
    analysis_df = subset_df.copy()
    for target in available_targets:
        if target not in analysis_df.columns:
            analysis_df[target] = df[target]

    # Get numeric columns only
    numeric_df = analysis_df.select_dtypes(include=[np.number])

    if numeric_df.shape[1] < 2:
        print(f"⚠️  Not enough numeric columns")
        continue

    # Store correlations for this group
    winning_correlations[group_name] = {}

    for target in available_targets:
        if target not in numeric_df.columns:
            continue

        print(f"\n🎯 Correlation with: {target}")
        print("-" * 80)

        # Calculate correlations with this target
        target_corrs = numeric_df.corr()[target]

        # CRITICAL: Remove the target itself and other winning metrics to avoid circular correlations
        metrics_to_exclude = [target] + [m for m in available_targets if m != target and m in target_corrs.index]
        target_corrs = target_corrs.drop(metrics_to_exclude, errors="ignore")

        # Remove NaN values
        target_corrs = target_corrs.dropna()

        # Sort by absolute value
        target_corrs_sorted = target_corrs.reindex(target_corrs.abs().sort_values(ascending=False).index)

        # Store for later
        winning_correlations[group_name][target] = target_corrs_sorted

        # Display top predictors
        print("\n🔥 TOP 10 POSITIVE PREDICTORS:")
        positive = target_corrs_sorted[target_corrs_sorted > 0].head(10)
        for idx, (metric, corr_val) in enumerate(positive.items(), 1):
            metric_short = metric[:60] + "..." if len(metric) > 60 else metric
            print(f"{idx:2d}. {corr_val:+.3f} | {metric_short}")

        print("\n❄️  TOP 10 NEGATIVE PREDICTORS:")
        negative = target_corrs_sorted[target_corrs_sorted < 0].head(10)
        for idx, (metric, corr_val) in enumerate(negative.items(), 1):
            metric_short = metric[:60] + "..." if len(metric) > 60 else metric
            print(f"{idx:2d}. {corr_val:+.3f} | {metric_short}")

print("\n" + "=" * 80)
print("✅ Winning formula analysis complete!")
print(f"📁 Results stored in 'winning_correlations' dictionary")
print("=" * 80)

# Summary: Find best predictors across ALL groups
print("\n" + "=" * 80)
print("🏆 BEST PREDICTORS ACROSS ALL GROUPS")
print("=" * 80)

for target in available_targets:
    print(f"\n🎯 {target}")
    print("-" * 80)

    all_corrs = []
    for group_name, targets in winning_correlations.items():
        if target in targets:
            for metric, corr_val in targets[target].items():
                all_corrs.append((group_name, metric, corr_val))

    # Sort by absolute correlation
    all_corrs.sort(key=lambda x: abs(x[2]), reverse=True)

    print("\nTOP 20 STRONGEST PREDICTORS (any group):")
    for idx, (group, metric, corr_val) in enumerate(all_corrs[:20], 1):
        metric_short = metric[:50] + "..." if len(metric) > 50 else metric
        print(f"{idx:2d}. {corr_val:+.3f} | [{group:15s}] {metric_short}")
