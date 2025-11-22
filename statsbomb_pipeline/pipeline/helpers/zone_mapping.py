# zone_mapping.py

import math

# ---------------------------------------------------------
# CONFIG: StatsBomb pitch is 120 x 80
# xThreat grid is 16 x 12 (192 zones)
# ---------------------------------------------------------

PITCH_LENGTH = 120
PITCH_WIDTH = 80

NX = 16  # zones along the length
NY = 12  # zones along the width

ZONE_LENGTH = PITCH_LENGTH / NX  # 120 / 16 = 7.5 meters per zone
ZONE_WIDTH = PITCH_WIDTH / NY  # 80 / 12  = 6.6667 meters per zone


def get_zone(x, y, NX=NX, NY=NY):
    """
    Convert raw StatsBomb location coordinates into a zone index.
    Zones are numbered row-major:

        row 0: zones 0 .. 15
        row 1: zones 16 .. 31
        ...
        row 11: zones 176 .. 191

    Returns None if x or y is missing.
    """

    if x is None or y is None:
        return None

    # column index (0 = left sideline)
    zx = int(x // (PITCH_LENGTH / NX))
    zx = min(max(zx, 0), NX - 1)  # clamp within grid

    # row index (0 = top of pitch)
    zy = int(y // (PITCH_WIDTH / NY))
    zy = min(max(zy, 0), NY - 1)

    # convert (row, col) → zone index
    zone_id = zy * NX + zx
    return int(zone_id)


# ---------------------------------------------------------
# OPTIONAL LOCAL TEST FUNCTION
# Pass in a list of parsed events (from your parser)
# ---------------------------------------------------------


def test_zone_mapping(parsed_events, n=20):
    """
    Prints the first n passes/carries/shots with their mapped zones.
    Useful for debugging or verifying your parser + grid logic.
    """
    print("Testing zone mapping on first", n, "events:\n")

    count = 0
    for row in parsed_events:
        if count >= n:
            break

        x, y = row.get("x"), row.get("y")
        end_x, end_y = row.get("end_x"), row.get("end_y")

        start_zone = get_zone(x, y)
        end_zone = get_zone(end_x, end_y) if end_x is not None else None

        print(
            {
                "event_type": row.get("event_type"),
                "team": row.get("team"),
                "x": x,
                "y": y,
                "end_x": end_x,
                "end_y": end_y,
                "start_zone": start_zone,
                "end_zone": end_zone,
            }
        )

        count += 1
