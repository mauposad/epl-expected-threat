"""StatsBomb pitch geometry.

StatsBomb uses a 120 x 80 yard pitch with the origin at the top-left corner, and
it normalises every event so the team in possession attacks left to right
(towards x = 120). No flipping is needed before comparing teams.
"""

import numpy as np

PITCH_LENGTH = 120.0
PITCH_WIDTH = 80.0

# Penalty area of the attacked goal.
BOX_MIN_X = 102.0
BOX_MIN_Y = 18.0
BOX_MAX_Y = 62.0

FINAL_THIRD_X = 80.0


def zone_index(x, y, nx: int = 16, ny: int = 12) -> np.ndarray:
    """Map pitch coordinates to a row-major zone index on an ``ny`` x ``nx`` grid.

    Column 0 is the team's own goal line and row 0 is the top touchline, so
    ``index = row * nx + col``. Coordinates on or beyond the pitch edge are
    clamped into the outermost zone. Missing coordinates map to -1.
    """
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    missing = np.isnan(x) | np.isnan(y)

    col = np.clip(np.floor(np.nan_to_num(x) / (PITCH_LENGTH / nx)), 0, nx - 1).astype(int)
    row = np.clip(np.floor(np.nan_to_num(y) / (PITCH_WIDTH / ny)), 0, ny - 1).astype(int)

    idx = row * nx + col
    return np.where(missing, -1, idx)


def in_box(x, y) -> np.ndarray:
    """True where a location is inside the attacked penalty area."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    return (x > BOX_MIN_X) & (y > BOX_MIN_Y) & (y < BOX_MAX_Y)
