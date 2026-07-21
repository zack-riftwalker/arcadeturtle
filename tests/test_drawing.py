"""تست‌های headless فاز ۴ (بدون ساخت arcade.Text که به پنجره نیاز دارد)."""

import pytest

import arcadeturtle
from arcadeturtle import api
from arcadeturtle._engine import get_engine, reset_engine
from arcadeturtle._text_fa import has_persian, shape_text


@pytest.fixture(autouse=True)
def fresh_engine():
    reset_engine()
    api._default_turtle = None
    yield
    reset_engine()
    api._default_turtle = None


def drain(engine, seconds=120.0, step=1 / 60):
    t = 0.0
    while t < seconds and (engine.queue or engine.active_cmd is not None):
        engine.tick(step)
        t += step


def test_full_circle_returns_to_start():
    arcadeturtle.speed(0)
    arcadeturtle.circle(50)
    assert arcadeturtle.position() == pytest.approx((0, 0), abs=1e-6)
    assert arcadeturtle.heading() == pytest.approx(0, abs=1e-6) or \
        arcadeturtle.heading() == pytest.approx(360, abs=1e-6)


def test_half_circle_heading():
    arcadeturtle.speed(0)
    arcadeturtle.circle(50, 180)
    # بعد از نیم‌دایره، جهت ۱۸۰ درجه چرخیده و y = قطر
    assert arcadeturtle.heading() == pytest.approx(180)
    assert arcadeturtle.ycor() == pytest.approx(100)


def test_negative_radius_turns_clockwise():
    arcadeturtle.speed(0)
    arcadeturtle.circle(-50, 90)
    assert arcadeturtle.heading() == pytest.approx(270)


def test_fill_collects_path_and_bakes_polygon():
    arcadeturtle.speed(0)
    arcadeturtle.fillcolor("red")
    arcadeturtle.begin_fill()
    for _ in range(4):
        arcadeturtle.forward(100)
        arcadeturtle.left(90)
    arcadeturtle.end_fill()
    eng = get_engine()
    eng.tick(1 / 60)
    assert len(eng.renderer.fills) == 1
    assert len(eng.renderer.fills[0].points) == 5  # نقطه شروع + ۴ گوشه
    assert eng.renderer.fills[0].color == (255, 0, 0)


def test_dot_bakes_circle_fill():
    arcadeturtle.speed(0)
    arcadeturtle.dot(20, "blue")
    eng = get_engine()
    eng.tick(1 / 60)
    assert len(eng.renderer.fills) == 1
    assert eng.renderer.fills[0].color == (0, 0, 255)


def test_stamp_and_clearstamp():
    arcadeturtle.speed(0)
    sid = arcadeturtle.stamp()
    eng = get_engine()
    eng.tick(1 / 60)
    assert len(eng.renderer.stamps) == 1
    arcadeturtle.clearstamp(sid)
    eng.tick(1 / 60)
    assert eng.renderer.stamps == []


def test_color_sets_both():
    arcadeturtle.color("green")
    assert arcadeturtle.pencolor() == "green"
    assert arcadeturtle.fillcolor() == "green"
    arcadeturtle.color("red", "yellow")
    assert (arcadeturtle.pencolor(), arcadeturtle.fillcolor()) == ("red", "yellow")


def test_shapesize():
    arcadeturtle.shapesize(2)
    assert arcadeturtle.shapesize() == (2, 2, 1)
    arcadeturtle.shapesize(1.5, 3)
    assert arcadeturtle.shapesize() == (1.5, 3, 1)


def test_persian_detection_and_shaping():
    assert has_persian("سلام")
    assert not has_persian("hello")
    shaped = shape_text("سلام")
    assert shaped != "سلام"  # حروف باید به فرم متصل تبدیل شده باشند
    assert shape_text("hello") == "hello"


def test_hex_and_float_colors():
    arcadeturtle.pencolor("#ff8000")
    assert get_engine().turtles[0].logical.pen_color == (255, 128, 0)
    arcadeturtle.pencolor((1.0, 0.0, 0.5))  # حالت colormode(1.0)
    assert get_engine().turtles[0].logical.pen_color == (255, 0, 128)
