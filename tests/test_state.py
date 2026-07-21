import pytest

from arcadeturtle._state import TurtleState


def test_forward_east():
    s = TurtleState()
    old, new = s.move_forward(100)
    assert old == (0, 0)
    assert s.x == pytest.approx(100)
    assert s.y == pytest.approx(0, abs=1e-9)


def test_left_then_forward():
    s = TurtleState()
    s.move_forward(100)
    s.rotate(90)
    s.move_forward(50)
    assert s.x == pytest.approx(100)
    assert s.y == pytest.approx(50)


def test_rotate_normalization():
    s = TurtleState()
    s.rotate(-90)
    assert s.heading == pytest.approx(270)
    s.rotate(450)
    assert s.heading == pytest.approx(0)


def test_backward_is_negative_forward():
    s = TurtleState()
    s.move_forward(-60)
    assert s.x == pytest.approx(-60)


def test_goto_returns_old_and_new():
    s = TurtleState()
    old, new = s.goto(30, -40)
    assert old == (0, 0)
    assert new == (30, -40)


def test_towards_and_distance():
    s = TurtleState()
    assert s.towards(0, 100) == pytest.approx(90)
    assert s.towards(-100, 0) == pytest.approx(180)
    assert s.distance_to(3, 4) == pytest.approx(5)


def test_copy_pose_is_independent():
    s = TurtleState()
    c = s.copy_pose()
    s.move_forward(100)
    assert c.x == 0
    s.fill_points.append((1, 1))
    assert c.fill_points == []
