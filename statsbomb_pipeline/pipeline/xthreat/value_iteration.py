# value_iteration.py

import numpy as np
from statsbomb_pipeline.pipeline.xthreat.transition_builder import (
    build_transitions,
    NUM_ZONES,
)


def build_value_function(
    transitions: np.ndarray,
    shot_counts: np.ndarray,
    shot_xg: np.ndarray,
    gamma: float = 0.99,
    tol: float = 1e-6,
    max_iters: int = 5000,
) -> np.ndarray:
    """
    Compute the xThreat value function for each zone using value iteration.

    Args:
        transitions: (NUM_ZONES x NUM_ZONES) matrix of zone→zone transition counts.
        shot_counts: length NUM_ZONES, number of shots taken from each zone.
        shot_xg:     length NUM_ZONES, total xG of shots taken from each zone.
        gamma:       discount factor in [0,1]. 0.99 is a good default.
        tol:         convergence tolerance.
        max_iters:   max number of iterations.

    Returns:
        values: length NUM_ZONES array of xThreat value per zone.
    """

    # Total actions from each zone: passes/carries + shots
    actions_from_zone = transitions.sum(axis=1) + shot_counts

    # Avoid division by zero
    nonzero_mask = actions_from_zone > 0

    # Immediate reward: expected xG directly from this zone
    # r[z] = total_xg[z] / total_actions[z]
    rewards = np.zeros(NUM_ZONES, dtype=float)
    rewards[nonzero_mask] = shot_xg[nonzero_mask] / actions_from_zone[nonzero_mask]

    # Transition probabilities P[z, k] = transitions[z,k] / total_actions[z]
    P = np.zeros_like(transitions, dtype=float)
    P[nonzero_mask, :] = (
        transitions[nonzero_mask, :] / actions_from_zone[nonzero_mask, None]
    )

    # Initialize values to zero
    values = np.zeros(NUM_ZONES, dtype=float)

    for it in range(max_iters):
        # Bellman update: V_new = r + gamma * P V
        new_values = rewards + gamma * P.dot(values)

        # Check convergence
        delta = np.max(np.abs(new_values - values))
        values = new_values

        if delta < tol:
            print(
                f"Value iteration converged in {it + 1} iterations (delta={delta:.2e})"
            )
            break
    else:
        print(f"Value iteration reached max_iters={max_iters} with delta={delta:.2e}")

    return values


# ---------------------------------------------------------
# LOCAL TEST: run on a single parsed match
# ---------------------------------------------------------


def test_value_iteration(parsed_events):
    """
    Given parsed events (from events_parser.parse_event_file),
    build transitions, run value iteration, and print a summary.
    """
    transitions, shot_counts, shot_xg = build_transitions(parsed_events)

    print("Transition matrix shape:", transitions.shape)
    print("Total transitions:", transitions.sum())
    print("Total shots:", shot_counts.sum())
    print("Total xG:", shot_xg.sum())

    values = build_value_function(transitions, shot_counts, shot_xg)

    print("\nSample of zone values (first 20):")
    print(values[:20])

    # Show top 10 most valuable zones
    top_indices = np.argsort(values)[::-1][:10]
    print("\nTop 10 zones by xThreat value:")
    for idx in top_indices:
        print(f"Zone {idx}: {values[idx]:.4f}")

    return values
