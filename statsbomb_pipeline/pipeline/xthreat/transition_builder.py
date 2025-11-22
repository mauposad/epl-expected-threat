# transition_builder.py

import numpy as np
from statsbomb_pipeline.pipeline.xthreat.zone_mapping import get_zone, NX, NY

# Number of zones
NUM_ZONES = NX * NY  # 16 * 12 = 192


def build_transitions(parsed_events):
    """
    Construct the transition counts and shot values
    for xThreat using parsed StatsBomb events.

    Returns:
        transitions: 192x192 matrix of zone→zone counts
        shot_counts: length-192 array of shots taken from each zone
        shot_xg:     length-192 array of total xG from each zone
    """

    # Initialize transition count matrix
    transitions = np.zeros((NUM_ZONES, NUM_ZONES), dtype=float)

    # Shot value storage
    shot_counts = np.zeros(NUM_ZONES, dtype=float)
    shot_xg = np.zeros(NUM_ZONES, dtype=float)

    # Loop through each parsed event
    for row in parsed_events:
        etype = row.get("event_type")
        x, y = row.get("x"), row.get("y")

        # Map start zone
        start_zone = get_zone(x, y)

        # -------------------------
        # HANDLE PASS / CARRY
        # -------------------------
        if etype in ("Pass", "Carry"):
            end_x = row.get("end_x")
            end_y = row.get("end_y")

            end_zone = get_zone(end_x, end_y)

            if start_zone is not None and end_zone is not None:
                transitions[start_zone][end_zone] += 1

        # -------------------------
        # HANDLE SHOTS
        # -------------------------
        elif etype == "Shot":
            if start_zone is not None:
                shot_counts[start_zone] += 1

                xg = row.get("xg")
                if xg is not None:
                    shot_xg[start_zone] += xg

    return transitions, shot_counts, shot_xg


# ------------------------------------------------------------------
# LOCAL TESTING FUNCTION
# ------------------------------------------------------------------


def test_transitions(parsed_events):
    """
    Print a summary of transition statistics
    to ensure the transition matrix is building correctly.
    """
    transitions, shot_counts, shot_xg = build_transitions(parsed_events)

    print("Transition matrix shape:", transitions.shape)
    print("\nSample of non-zero transitions:")

    # show some transitions
    nz = np.argwhere(transitions > 0)
    for i, j in nz[:20]:  # first 20 non-zero transitions
        print(f"Zone {i} → {j}: {transitions[i][j]}")

    print("\nShot counts (first 20 zones):")
    print(shot_counts[:20])

    print("\nShot xG (first 20 zones):")
    print(shot_xg[:20])

    return transitions, shot_counts, shot_xg
