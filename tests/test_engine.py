"""تست موتور بدون پنجره — tick مستقیم صدا زده می‌شود (نیازی به OpenGL نیست)."""

import pytest

import arcadeturtle
from arcadeturtle import api
from arcadeturtle._engine import get_engine, reset_engine
from arcadeturtle._errors import ArcadeTurtleError


@pytest.fixture(autouse=True)
def fresh_engine():
    reset_engine()
    api._default_turtle = None
    yield
    reset_engine()
    api._default_turtle = None


def drain(engine, seconds=60.0, step=1 / 60):
    """شبیه‌سازی فریم‌ها تا خالی‌شدن صف."""
    t = 0.0
    while t < seconds and (engine.queue or engine.active_cmd is not None):
        engine.tick(step)
        t += step


def test_logical_state_updates_immediately():
    arcadeturtle.forward(100)
    assert arcadeturtle.position() == pytest.approx((100, 0))
    # صف هنوز پخش نشده ولی کوئری درست است
    assert get_engine().queue


def test_visual_catches_up_after_ticks():
    arcadeturtle.forward(100)
    arcadeturtle.left(90)
    arcadeturtle.forward(50)
    eng = get_engine()
    drain(eng)
    v = eng.turtles[0].visual
    assert (v.x, v.y) == (pytest.approx(100), pytest.approx(50))
    assert v.heading == pytest.approx(90)
    assert len(eng.renderer.finished_lines) == 2


def test_penup_draws_no_line():
    arcadeturtle.penup()
    arcadeturtle.forward(100)
    eng = get_engine()
    drain(eng)
    assert eng.renderer.finished_lines == []
    assert eng.turtles[0].visual.x == pytest.approx(100)


def test_speed_zero_is_instant():
    arcadeturtle.speed(0)
    arcadeturtle.forward(500)
    eng = get_engine()
    eng.tick(1 / 60)  # یک فریم کافی است
    assert eng.turtles[0].visual.x == pytest.approx(500)
    assert not eng.queue and eng.active_cmd is None


def test_square_geometry():
    arcadeturtle.speed(0)
    for _ in range(4):
        arcadeturtle.forward(100)
        arcadeturtle.left(90)
    eng = get_engine()
    eng.tick(1 / 60)
    assert arcadeturtle.position() == pytest.approx((0, 0), abs=1e-6)
    assert arcadeturtle.heading() == pytest.approx(0)
    assert len(eng.renderer.finished_lines) == 4


def test_setheading_shortest_path():
    arcadeturtle.setheading(270)
    eng = get_engine()
    cmd = eng.queue[-1]
    assert cmd.delta == pytest.approx(-90)  # نه +270


def test_backward_and_aliases():
    arcadeturtle.bk(50)
    assert arcadeturtle.xcor() == pytest.approx(-50)
    arcadeturtle.rt(90)
    assert arcadeturtle.heading() == pytest.approx(270)


def test_invalid_color_message_is_friendly():
    with pytest.raises(ArcadeTurtleError) as e:
        arcadeturtle.pencolor("ghermez")
    assert "نمی‌شناسم" in str(e.value)


def test_invalid_number_message():
    with pytest.raises(ArcadeTurtleError) as e:
        arcadeturtle.forward("صد")
    assert "عدد" in str(e.value)


def test_speed_names():
    arcadeturtle.speed("fastest")
    assert arcadeturtle.speed() == 0
    arcadeturtle.speed("normal")
    assert arcadeturtle.speed() == 6


def test_goto_tuple_form():
    arcadeturtle.goto((30, 40))
    assert arcadeturtle.position() == pytest.approx((30, 40))
    assert arcadeturtle.distance(0, 0) == pytest.approx(50)


def test_queue_order_across_turtles():
    from arcadeturtle import Turtle
    a = Turtle()
    b = Turtle()
    a.speed(0)
    b.speed(0)
    a.forward(10)
    b.forward(20)
    a.forward(10)
    eng = get_engine()
    eng.tick(1 / 60)
    assert eng.turtles[a._id].visual.x == pytest.approx(20)
    assert eng.turtles[b._id].visual.x == pytest.approx(20)
