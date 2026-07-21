import pytest

import arcadeturtle
from arcadeturtle import Screen, Turtle, api
from arcadeturtle._engine import get_engine, reset_engine
from arcadeturtle._errors import ArcadeTurtleError
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


def test_screen_is_singleton():
    assert Screen() is Screen()


def test_setup_sets_size_before_window():
    s = Screen()
    s.setup(600, 600)
    eng = get_engine()
    assert (eng.pending_width, eng.pending_height) == (600, 600)
    assert (eng.renderer.width, eng.renderer.height) == (600, 600)
    assert s.window_width() == 600


def test_setup_fraction_not_supported():
    with pytest.raises(ArcadeTurtleError):
        Screen().setup(0.5, 0.5)


def test_screen_events_bind_same_registry():
    import arcade.key
    hits = []
    s = Screen()
    s.listen()
    s.onkeypress(lambda: hits.append(1), "w")
    get_engine().events.handle_key_press(arcade.key.W)
    assert hits == [1]


def test_unsupported_features_raise_clean_error():
    s = Screen()
    for call in (s.setworldcoordinates, s.bgpic, s.register_shape):
        with pytest.raises(ArcadeTurtleError) as e:
            call()
        assert "پشتیبانی نمی‌شود" in str(e.value)


def test_multiple_turtles_independent_state():
    a = Turtle()
    b = Turtle()
    a.speed(0)
    b.speed(0)
    a.pencolor("red")
    b.pencolor("blue")
    a.forward(100)
    b.left(90)
    b.forward(50)
    assert a.position() == pytest.approx((100, 0))
    assert b.position() == pytest.approx((0, 50))
    assert a.heading() == 0 and b.heading() == 90
    eng = get_engine()
    eng.tick(1 / 60)
    lines = eng.renderer.finished_lines
    assert len(lines) == 2
    assert {ln.color for ln in lines} == {(255, 0, 0), (0, 0, 255)}


def test_distance_between_turtles():
    a = Turtle()
    b = Turtle()
    a.speed(0)
    b.speed(0)
    b.goto(30, 40)
    assert a.distance(b) == pytest.approx(50)
    assert a.towards(b) == pytest.approx(pytest.approx(53.13010235))


def test_turtle_constructor_shape_and_visible():
    t = Turtle(shape="square", visible=False)
    assert t.shape() == "square"
    assert not t.isvisible()


def test_screen_tracer_roundtrip():
    s = Screen()
    s.tracer(0)
    assert s.tracer() == 0
    assert arcadeturtle.tracer() == 0


def test_screen_reset_resets_every_turtle():
    """resetscreen استاندارد روی همه لاک‌پشت‌ها reset() می‌زند، نه فقط پاک‌کردن."""
    a, b = Turtle(), Turtle()
    a.speed(0)
    b.speed(0)
    a.pencolor("red")
    a.forward(100)
    b.left(90)
    b.forward(50)
    b.pensize(7)
    eng = get_engine()
    eng.tick(1 / 60)
    assert eng.renderer.finished_lines  # چیزی کشیده شده

    Screen().reset()
    eng.tick(1 / 60)

    for t in (a, b):
        assert t.position() == pytest.approx((0, 0))
        assert t.heading() == pytest.approx(0)
        assert t.pencolor() == "black"
        assert t.pensize() == 1
        assert t.isdown()
    assert eng.renderer.finished_lines == []


def test_screen_clear_leaves_turtles_alone():
    """در مقابل reset: clear فقط نقاشی‌ها را پاک می‌کند."""
    t = Turtle()
    t.speed(0)
    t.forward(100)
    eng = get_engine()
    eng.tick(1 / 60)

    Screen().clear()
    eng.tick(1 / 60)

    assert eng.renderer.finished_lines == []
    assert t.position() == pytest.approx((100, 0)), "clear نباید لاک‌پشت را جابه‌جا کند"
