"""Expected Threat (xT), following Karun Singh's formulation.

The pitch is split into a grid. For each zone z the model estimates, from a full
season of actions:

    s(z)    probability the player in possession shoots from z
    m(z)    probability they move the ball (pass or carry) instead, = 1 - s(z)
    g(z)    expected goal value of a shot from z (mean StatsBomb xG)
    T(z,k)  probability a move from z ends successfully in zone k

and solves the fixed point

    xT(z) = s(z) * g(z) + m(z) * sum_k T(z,k) * xT(k)

by iteration. Failed moves contribute nothing to the sum, which is how losing
the ball is penalised. A successful move from zone a to zone b is credited with
xT(b) - xT(a); unsuccessful moves are credited with 0.

Reference: https://karun.in/blog/expected-threat.html
"""

import numpy as np
import pandas as pd

from epl_xt.events import successful_mask
from epl_xt.pitch import zone_index


class ExpectedThreat:
    def __init__(self, nx: int = 16, ny: int = 12, tol: float = 1e-6, max_iter: int = 1000):
        self.nx = nx
        self.ny = ny
        self.tol = tol
        self.max_iter = max_iter

    @property
    def n_zones(self) -> int:
        return self.nx * self.ny

    def _zones(self, x, y) -> np.ndarray:
        return zone_index(x, y, self.nx, self.ny)

    def fit(self, actions: pd.DataFrame) -> "ExpectedThreat":
        """Estimate the xT surface from a table of actions.

        ``actions`` needs ``type``, ``x``, ``y``, ``end_x``, ``end_y``,
        ``successful`` and ``xg`` columns, as produced by
        :func:`epl_xt.events.parse_events`. Pass in open-play actions only:
        penalties and set-piece restarts would distort the zone estimates.
        """
        n = self.n_zones
        is_move = actions["type"].isin(["Pass", "Carry"]).to_numpy()
        is_shot = (actions["type"] == "Shot").to_numpy()

        start = self._zones(actions["x"], actions["y"])
        end = self._zones(actions["end_x"], actions["end_y"])
        ok = start >= 0

        move_counts = np.bincount(start[is_move & ok], minlength=n).astype(float)
        shot_counts = np.bincount(start[is_shot & ok], minlength=n).astype(float)
        shot_xg = np.bincount(
            start[is_shot & ok],
            weights=actions.loc[is_shot & ok, "xg"].fillna(0).to_numpy(),
            minlength=n,
        )

        successful = successful_mask(actions)
        good_move = is_move & ok & successful & (end >= 0)
        transitions = np.zeros((n, n))
        np.add.at(transitions, (start[good_move], end[good_move]), 1.0)

        total = move_counts + shot_counts
        with np.errstate(divide="ignore", invalid="ignore"):
            self.shot_prob_ = np.where(total > 0, shot_counts / total, 0.0)
            self.move_prob_ = np.where(total > 0, move_counts / total, 0.0)
            self.goal_prob_ = np.where(shot_counts > 0, shot_xg / shot_counts, 0.0)
            # Rows are divided by all moves, not just successful ones, so each
            # row sums to that zone's move success rate rather than to 1.
            self.transition_ = np.where(move_counts[:, None] > 0, transitions / move_counts[:, None], 0.0)

        xt = np.zeros(n)
        payoff = self.shot_prob_ * self.goal_prob_
        for n_iter in range(1, self.max_iter + 1):  # noqa: B007 (kept as n_iter_)
            new = payoff + self.move_prob_ * (self.transition_ @ xt)
            delta = np.abs(new - xt).max()
            xt = new
            if delta < self.tol:
                break
        self.n_iter_ = n_iter
        self.values_ = xt
        return self

    @property
    def grid(self) -> np.ndarray:
        """xT values as a (ny, nx) array; column 0 is the defending goal line."""
        return self.values_.reshape(self.ny, self.nx)

    def value_at(self, x, y) -> np.ndarray:
        """xT of the zone containing each location (NaN where location is missing)."""
        z = self._zones(x, y)
        return np.where(z >= 0, self.values_[np.maximum(z, 0)], np.nan)

    def rate(self, actions: pd.DataFrame) -> np.ndarray:
        """xT added by each action: end value minus start value for successful moves, else 0."""
        is_move = actions["type"].isin(["Pass", "Carry"]).to_numpy()
        successful = successful_mask(actions)
        delta = self.value_at(actions["end_x"], actions["end_y"]) - self.value_at(actions["x"], actions["y"])
        return np.where(is_move & successful & ~np.isnan(delta), delta, 0.0)
