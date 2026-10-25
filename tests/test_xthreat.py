import numpy as np
import pandas as pd
import pytest

from epl_xt.xthreat import ExpectedThreat


def action(type_, x, y, end_x=None, end_y=None, successful=True, xg=None):
    return {
        "type": type_,
        "x": x,
        "y": y,
        "end_x": end_x,
        "end_y": end_y,
        "successful": successful if type_ != "Shot" else None,
        "xg": xg,
    }


@pytest.fixture
def corridor():
    """A 3 x 1 pitch where the ball always moves forward one zone, then a shot is taken.

    Zone 0 (x < 40): 1 successful pass to zone 1.
    Zone 1 (40-80):  1 successful pass to zone 2, 1 failed pass.
    Zone 2 (x > 80): 1 shot worth 0.3 xG and 1 successful pass back to zone 1.
    """
    rows = [
        action("Pass", 20, 40, 60, 40),
        action("Pass", 60, 40, 100, 40),
        action("Pass", 60, 40, 100, 40, successful=False),
        action("Shot", 100, 40, xg=0.3),
        action("Carry", 100, 40, 60, 40),
    ]
    return ExpectedThreat(nx=3, ny=1).fit(pd.DataFrame(rows))


def test_probabilities(corridor):
    np.testing.assert_allclose(corridor.shot_prob_, [0, 0, 0.5])
    np.testing.assert_allclose(corridor.goal_prob_, [0, 0, 0.3])
    # The failed pass counts as an attempted move but not as a transition.
    np.testing.assert_allclose(corridor.transition_[1], [0, 0, 0.5])


def test_values_solve_the_bellman_equation(corridor):
    s, m, g, T, v = (
        corridor.shot_prob_,
        corridor.move_prob_,
        corridor.goal_prob_,
        corridor.transition_,
        corridor.values_,
    )
    np.testing.assert_allclose(v, s * g + m * (T @ v), atol=1e-6)


def test_closed_form_values(corridor):
    # v2 = 0.5 * 0.3 + 0.5 * v1, v1 = 0.5 * v2 and v0 = v1, so v2 = 0.2 and v0 = v1 = 0.1.
    np.testing.assert_allclose(corridor.values_, [0.1, 0.1, 0.2], atol=1e-5)


def test_rate_credits_only_successful_moves(corridor):
    rated = pd.DataFrame(
        [
            action("Pass", 60, 40, 100, 40),
            action("Pass", 60, 40, 100, 40, successful=False),
            action("Carry", 100, 40, 60, 40),
            action("Shot", 100, 40, xg=0.3),
        ]
    )
    np.testing.assert_allclose(corridor.rate(rated), [0.1, 0.0, -0.1, 0.0], atol=1e-5)


def test_grid_shape():
    df = pd.DataFrame([action("Shot", 110, 40, xg=0.5)])
    assert ExpectedThreat().fit(df).grid.shape == (12, 16)
