# xthreat_aggregator.py

from typing import List, Dict
from collections import defaultdict


def aggregate_xthreat(scored_actions: List[Dict]):
    """
    Aggregates xThreat metrics for:
        - teams
        - players
        - possessions
        - match totals

    Args:
        scored_actions: list of dicts enriched with xThreat (from scorer)

    Returns:
        {
            "team_xT": dict,
            "player_xT": dict,
            "possession_xT": dict,
            "match_xT": float
        }
    """

    team_xT = defaultdict(float)
    player_xT = defaultdict(float)
    possession_xT = defaultdict(float)

    match_total = 0.0

    for row in scored_actions:
        xT = row.get("xThreat", 0.0)

        team = row.get("team")
        player = row.get("player_name")
        possession = row.get("possession")

        # update aggregates
        team_xT[team] += xT
        player_xT[player] += xT
        possession_xT[possession] += xT
        match_total += xT

    return {
        "team_xT": dict(team_xT),
        "player_xT": dict(player_xT),
        "possession_xT": dict(possession_xT),
        "match_xT": match_total,
    }


# ---------------------------------------------------------
# LOCAL TEST FUNCTION
# ---------------------------------------------------------


def test_xthreat_aggregation(scored_actions):
    results = aggregate_xthreat(scored_actions)

    print("\n================ TEAM xThreat ================")
    for team, xT in results["team_xT"].items():
        print(f"{team}: {xT:.4f}")

    print("\n================ PLAYER xThreat (Top 10) ================")
    sorted_players = sorted(
        results["player_xT"].items(), key=lambda x: x[1], reverse=True
    )
    for p, xT in sorted_players[:10]:
        print(f"{p}: {xT:.4f}")

    print("\n================ POSSESSION xThreat (first 10) ================")
    for k in sorted(list(results["possession_xT"].keys()))[:10]:
        print(f"Possession {k}: {results['possession_xT'][k]:.4f}")

    print("\n================ MATCH TOTAL xThreat ================")
    print(results["match_xT"])

    return results
