import pytest

from arcadeturtle._coords import to_arcade, to_turtle


def test_origin_maps_to_center():
    assert to_arcade(0, 0, 800, 600) == (400, 300)


def test_roundtrip():
    ax, ay = to_arcade(-120, 75, 640, 480)
    assert to_turtle(ax, ay, 640, 480) == pytest.approx((-120, 75))


def test_top_right_quadrant():
    assert to_arcade(100, 100, 800, 600) == (500, 400)
