import pytest

import arcadeturtle
from arcadeturtle import Pen, RawPen, RawTurtle, Screen, Turtle, api
from arcadeturtle._engine import get_engine, reset_engine
from arcadeturtle._errors import ArcadeTurtleError
from arcadeturtle.screen import ScrolledCanvas, TurtleScreen, reset_screen_singleton


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


# ---------- 10.1: وصل‌کردن سطح ماژول + alias کلاس‌ها ----------

def test_module_level_window_functions_forward_to_screen():
    arcadeturtle.setup(500, 400)
    assert arcadeturtle.window_width() == 500
    assert arcadeturtle.window_height() == 400
    assert arcadeturtle.screensize() == (500, 400)


def test_turtles_returns_live_turtle_objects():
    assert arcadeturtle.turtles() == []
    a = Turtle()
    b = Turtle()
    assert set(arcadeturtle.turtles()) == {a, b}
    assert Screen().turtles() == arcadeturtle.turtles()


def test_delay_getter_setter_roundtrip():
    assert arcadeturtle.delay() == 10  # پیش‌فرض stdlib
    arcadeturtle.delay(25)
    assert arcadeturtle.delay() == 25
    assert Screen().delay() == 25


def test_mode_getter_and_unsupported_change():
    assert arcadeturtle.mode() == "standard"
    with pytest.raises(ArcadeTurtleError) as e:
        arcadeturtle.mode("logo")
    assert "پشتیبانی نمی‌شود" in str(e.value)


def test_getcanvas_raises_friendly_error():
    with pytest.raises(ArcadeTurtleError):
        arcadeturtle.getcanvas()
    with pytest.raises(ArcadeTurtleError):
        Screen().getcanvas()


def test_module_level_unsupported_forwarding():
    """bgpic/register_shape/setworldcoordinates باید هم در سطح ماژول در دسترس
    باشند و هم همان خطای مهربانِ Screen را بدهند."""
    for fn in (
        lambda: arcadeturtle.bgpic("x.png"),
        lambda: arcadeturtle.register_shape("x", ((0, 0),)),
        lambda: arcadeturtle.addshape("x", ((0, 0),)),
        lambda: arcadeturtle.setworldcoordinates(0, 0, 1, 1),
    ):
        with pytest.raises(ArcadeTurtleError):
            fn()


def test_bye_and_clearscreen_resetscreen_forward():
    Screen().setup(400, 300)
    t = Turtle()
    t.speed(0)
    t.forward(50)
    get_engine().tick(1 / 60)
    arcadeturtle.clearscreen()
    get_engine().tick(1 / 60)
    assert get_engine().renderer.finished_lines == []

    t.forward(50)
    get_engine().tick(1 / 60)
    arcadeturtle.resetscreen()
    get_engine().tick(1 / 60)
    assert t.position() == pytest.approx((0, 0))

    arcadeturtle.bye()  # نباید خطا بدهد حتی وقتی پنجره‌ای ساخته نشده


def test_pen_is_turtle_class():
    assert Pen is Turtle
    p = Pen()
    assert isinstance(p, Turtle)


def test_rawturtle_ignores_canvas_argument():
    rt = RawTurtle(canvas=object())
    assert isinstance(rt, Turtle)
    rt.speed(0)
    rt.forward(10)
    assert rt.position() == pytest.approx((10, 0))


def test_rawpen_is_subclass_of_rawturtle():
    assert issubclass(RawPen, RawTurtle)
    assert isinstance(RawPen(), RawTurtle)


def test_turtlescreen_and_scrolledcanvas_raise_friendly_error():
    with pytest.raises(ArcadeTurtleError):
        TurtleScreen()
    with pytest.raises(ArcadeTurtleError):
        ScrolledCanvas()


def test_terminator_importable_and_is_exception():
    assert issubclass(arcadeturtle.Terminator, Exception)
