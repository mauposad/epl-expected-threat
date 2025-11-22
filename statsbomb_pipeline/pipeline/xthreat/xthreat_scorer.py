# xthreat_scorer.py

from statsbomb_pipeline.pipeline.xthreat.zone_mapping import get_zone
from typing import List, Dict


def score_actions_with_xthreat(parsed_events: List[Dict], zone_values):
    """
    Assign xThreat to each pass or carry action.

    Args:
        parsed_events: list of event dicts from events_parser.parse_event_file
        zone_values:   array-like, xThreat value per zone (length 192)

    Returns:
        scored_events: same list but each pass/carry has a 'xThreat' field.
    """

    scored = []

    for row in parsed_events:
        etype = row.get("event_type")

        if etype not in ("Pass", "Carry"):
            # Non-progressive events: just append without xT
            scored.append({**row, "xThreat": 0.0})
            continue

        # Map start and end zones
        start_zone = get_zone(row.get("x"), row.get("y"))
        end_zone = get_zone(row.get("end_x"), row.get("end_y"))

        if start_zone is None or end_zone is None:
            xT = 0.0
        else:
            xT = zone_values[end_zone] - zone_values[start_zone]

        # Add score to row
        new_row = dict(row)
        new_row["start_zone"] = start_zone
        new_row["end_zone"] = end_zone
        new_row["xThreat"] = float(xT)

        scored.append(new_row)

    return scored


# ---------------------------------------------------------
# LOCAL TEST FUNCTION
# ---------------------------------------------------------


def test_xthreat_scoring(parsed_events, zone_values, n=20):
    """
    Test per-action xThreat scoring and print sample output.
    """
    scored = score_actions_with_xthreat(parsed_events, zone_values)

    print("\nSample scored actions:\n")
    count = 0
    for row in scored:
        if row["event_type"] in ("Pass", "Carry") and count < n:
            print(
                {
                    "event_type": row["event_type"],
                    "team": row["team"],
                    "start_zone": row.get("start_zone"),
                    "end_zone": row.get("end_zone"),
                    "xThreat": row["xThreat"],
                }
            )
            count += 1

    # Summaries
    total_xT = sum(r["xThreat"] for r in scored)
    print(f"\nTotal xThreat in match: {total_xT:.4f}")

    return scored
