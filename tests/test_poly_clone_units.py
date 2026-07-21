"""فاز ۱۰.۶: begin_poly/end_poly/get_poly، clone، getturtle/getpen، pen()،
degrees/radians."""

import math

import pytest

import arcadeturtle
from arcadeturtle import Turtle, api
from arcadeturtle._engine import get_engine, reset_engine
from arcadeturtle.screen import reset_screen_singleton


@pytest.fixture(autouse=True)
def fresh():
    reset_engine()
    reset_screen_singleton()
    api._default_turtle = None
    yield
    reset_engine()
    reset_screen_singleton()
    api._default_turtle = None


# ---------- getturtle / getpen ----------

def test_getturtle_and_getpen_return_self():
    t = Turtle()
    assert t.getturtle() is t
    assert t.getpen() is t


# ---------- pen() ----------

def test_pen_getter_returns_full_snapshot():
    t = Turtle()
    t.pen(fillcolor="black", pencolor="red", pensize=10)
    snap = t.pen()
    assert snap["pencolor"] == "red"
    assert snap["fillcolor"] == "black"
    assert snap["pensize"] == 10
    assert snap["pendown"] is True
    assert snap["shown"] is True


def test_pen_setter_restores_snapshot_with_override():
    """دقیقاً مثل مثال docstring خودِ stdlib."""
    t = Turtle()
    t.pen(fillcolor="black", pencolor="red", pensize=10)
    snapshot = t.pen()
    t.color("yellow", "white")
    t.penup()
    assert t.pen()["pencolor"] == "yellow"
    assert t.pen()["pendown"] is False

    t.pen(snapshot, fillcolor="green")
    restored = t.pen()
    assert restored["pencolor"] == "red"
    assert restored["pendown"] is True
    assert restored["fillcolor"] == "green"  # override باید برنده باشد


def test_pen_shown_key_toggles_visibility():
    t = Turtle()
    t.pen(shown=False)
    assert not t.isvisible()
    t.pen(shown=True)
    assert t.isvisible()


# ---------- begin_poly / end_poly / get_poly ----------

def test_get_poly_none_before_begin_poly():
    t = Turtle()
    assert t.get_poly() is None


def test_poly_records_vertices_visited_while_active():
    t = Turtle()
    t.speed(0)
    t.begin_poly()
    t.forward(50)
    t.left(90)
    t.forward(50)
    t.end_poly()
    assert t.get_poly() == ((0.0, 0.0), (50.0, 0.0), (50.0, 50.0))


def test_poly_stops_recording_after_end_poly():
    t = Turtle()
    t.speed(0)
    t.begin_poly()
    t.forward(10)
    t.end_poly()
    before = t.get_poly()
    t.forward(999)
    assert t.get_poly() == before


def test_poly_can_be_registered_as_a_shape():
    """همان الگوی docstring خودِ stdlib: register_shape(name, get_poly())."""
    from arcadeturtle import Screen

    t = Turtle()
    t.speed(0)
    t.begin_poly()
    t.forward(20)
    t.left(120)
    t.forward(20)
    t.left(120)
    t.forward(20)
    t.end_poly()
    Screen().register_shape("myTriangle", t.get_poly())
    assert "myTriangle" in Screen().getshapes()


# ---------- clone ----------

def test_clone_copies_pose_and_appearance_independently():
    t = Turtle(shape="circle")
    t.speed(0)
    t.penup()
    t.goto(30, 40)
    t.setheading(75)
    t.pencolor("purple")

    clone = t.clone()
    assert clone is not t
    assert clone.position() == pytest.approx(t.position())
    assert clone.heading() == pytest.approx(t.heading())
    assert clone.shape() == t.shape()
    assert clone.pencolor() == t.pencolor()

    clone.forward(100)
    assert t.position() == pytest.approx((30, 40)), "حرکت clone نباید اصلی را تکان بدهد"


def test_clone_is_tracked_by_turtles():
    t = Turtle()
    before = len(arcadeturtle.turtles())
    clone = t.clone()  # مرجع را نگه دار — turtle_objects یک WeakSet است
    assert len(arcadeturtle.turtles()) == before + 1
    assert clone in arcadeturtle.turtles()


def test_clone_has_independent_undo_stack():
    t = Turtle()
    t.speed(0)
    t.forward(10)
    clone = t.clone()
    assert clone.undobufferentries() == 0
    clone.forward(5)
    assert clone.undobufferentries() == 1
    assert t.undobufferentries() == 1  # دست‌نخورده


# ---------- degrees / radians ----------

def test_default_angle_unit_is_degrees():
    t = Turtle()
    t.left(90)
    assert t.heading() == pytest.approx(90)


def test_degrees_custom_fullcircle_like_stdlib_docstring():
    t = Turtle()
    t.left(90)
    t.degrees(400.0)
    assert t.heading() == pytest.approx(100)


def test_radians_matches_stdlib_docstring():
    t = Turtle()
    t.left(90)
    t.radians()
    assert t.heading() == pytest.approx(math.pi / 2)


def test_setheading_and_left_right_respect_current_unit():
    t = Turtle()
    t.radians()
    t.setheading(math.pi / 2)
    assert t.heading() == pytest.approx(math.pi / 2)
    t.left(math.pi)
    assert t.heading() == pytest.approx(math.pi / 2 + math.pi)


def test_towards_respects_current_unit():
    a = Turtle()
    b = Turtle()
    b.speed(0)
    b.goto(0, 10)
    a.radians()
    assert a.towards(b) == pytest.approx(math.pi / 2)


def test_angle_unit_is_per_turtle_not_global():
    a = Turtle()
    b = Turtle()
    a.radians()
    a.left(math.pi / 2)
    b.left(90)
    assert a.heading() == pytest.approx(math.pi / 2)
    assert b.heading() == pytest.approx(90)


def test_module_level_degrees_radians():
    arcadeturtle.left(90)
    assert arcadeturtle.heading() == pytest.approx(90)
    arcadeturtle.radians()
    assert arcadeturtle.heading() == pytest.approx(math.pi / 2)
