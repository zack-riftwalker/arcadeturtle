"""Vec2D: بردار زیرکلاس تاپل که position()/pos() برمی‌گرداند."""

import math

import pytest

from arcadeturtle._vec2d import Vec2D


def test_is_tuple_subclass_and_unpacks():
    v = Vec2D(3, 4)
    assert isinstance(v, tuple)
    x, y = v
    assert (x, y) == (3, 4)
    assert v == (3, 4)  # مقایسه با تاپل ساده هم کار کند


def test_add_and_sub():
    a = Vec2D(3, 4)
    b = Vec2D(1, 1)
    assert a + b == (4, 5)
    assert a - b == (2, 3)


def test_neg():
    assert -Vec2D(3, 4) == (-3, -4)


def test_scalar_mul_both_directions():
    v = Vec2D(3, 4)
    assert v * 2 == (6, 8)
    assert 2 * v == (6, 8)


def test_vector_dot_product():
    assert Vec2D(3, 4) * Vec2D(1, 1) == 7


def test_abs_is_length():
    assert abs(Vec2D(3, 4)) == pytest.approx(5.0)


def test_rotate_counterclockwise():
    v = Vec2D(1, 0)
    r = v.rotate(90)
    assert r[0] == pytest.approx(0, abs=1e-9)
    assert r[1] == pytest.approx(1, abs=1e-9)


def test_rotate_full_circle_returns_to_start():
    v = Vec2D(5, 2)
    r = v.rotate(360)
    assert r[0] == pytest.approx(5)
    assert r[1] == pytest.approx(2)


def test_repr_format():
    assert repr(Vec2D(3, 4)) == "(3.00,4.00)"
