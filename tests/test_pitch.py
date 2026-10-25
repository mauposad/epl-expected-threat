import numpy as np

from epl_xt.pitch import in_box, zone_index


def test_corners_map_to_first_and_last_zone():
    assert zone_index(0, 0) == 0
    assert zone_index(119.9, 79.9) == 16 * 12 - 1


def test_row_major_layout():
    # One zone is 7.5 x 6.67 yards; step one zone right, then one zone down.
    assert zone_index(7.5, 0) == 1
    assert zone_index(0, 6.7) == 16


def test_out_of_bounds_is_clamped():
    assert zone_index(125, 85) == zone_index(119.9, 79.9)
    assert zone_index(-3, -3) == 0


def test_missing_location_is_minus_one():
    out = zone_index([10, np.nan], [10, 10])
    assert out.tolist() == [zone_index(10, 10), -1]


def test_in_box():
    assert in_box(110, 40)
    assert not in_box(100, 40)  # outside the 18-yard line
    assert not in_box(110, 10)  # wide of the box
