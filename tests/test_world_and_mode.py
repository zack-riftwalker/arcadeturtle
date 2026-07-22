"""فاز ۱۰.۷: mode('logo'/'world')، setworldcoordinates، bgpic، textinput/numinput."""

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


@pytest.fixture
def test_png(tmp_path):
    from PIL import Image

    path = tmp_path / "bg.png"
    Image.new("RGBA", (40, 30), (10, 20, 30, 255)).save(path)
    return str(path)


# ---------- mode ----------

def test_mode_default_is_standard():
    assert Screen().mode() == "standard"


def test_mode_rejects_unknown_value():
    with pytest.raises(ArcadeTurtleError):
        Screen().mode("sideways")


def test_new_turtle_faces_east_in_standard_mode():
    t = Turtle()
    assert t.heading() == pytest.approx(0)


def test_new_turtle_faces_north_in_logo_mode():
    Screen().mode("logo")
    t = Turtle()
    assert t.heading() == pytest.approx(0)  # ۰ در logo یعنی شمال
    eng = get_engine()
    assert eng.turtles[t._id].logical.heading == pytest.approx(90)  # داخلی: شمال واقعی


def test_logo_mode_matches_stdlib_heading_table():
    """جدول دقیق docstring خودِ setheading: standard vs logo."""
    Screen().mode("logo")
    t = Turtle()
    t.speed(0)
    for logo_heading, internal in [(0, 90), (90, 0), (180, 270), (270, 180)]:
        t.setheading(logo_heading)
        assert t.heading() == pytest.approx(logo_heading)
        assert get_engine().turtles[t._id].logical.heading == pytest.approx(internal)


def test_left_and_right_always_rotate_the_same_physical_direction():
    """left/right در stdlib به mode بستگی ندارند — فقط عددِ نمایشیِ heading
    تفسیرش عوض می‌شود، نه جهت فیزیکیِ چرخش."""
    a = Turtle()
    a.speed(0)
    a.left(90)
    internal_standard = get_engine().turtles[a._id].logical.heading

    reset_engine()
    reset_screen_singleton()
    Screen().mode("logo")
    b = Turtle()
    b.speed(0)
    b.left(90)
    internal_logo = get_engine().turtles[b._id].logical.heading

    assert internal_standard == pytest.approx(90)
    assert internal_logo == pytest.approx(180)  # شمال(۹۰) + ۹۰ فیزیکی = ۱۸۰


def test_mode_change_resets_all_turtles():
    a, b = Turtle(), Turtle()
    a.speed(0)
    b.speed(0)
    a.forward(50)
    b.forward(50)
    Screen().mode("logo")
    assert a.position() == pytest.approx((0, 0))
    assert b.position() == pytest.approx((0, 0))


# ---------- setworldcoordinates ----------

def test_setworldcoordinates_switches_mode_to_world():
    Screen().setworldcoordinates(-50, -50, 50, 50)
    assert Screen().mode() == "world"


def test_setworldcoordinates_rejects_degenerate_rect():
    with pytest.raises(ArcadeTurtleError):
        Screen().setworldcoordinates(10, 10, 5, 20)
    with pytest.raises(ArcadeTurtleError):
        Screen().setworldcoordinates(0, 0, 0, 10)


def test_setworldcoordinates_scales_coordinates_correctly():
    Screen().setup(400, 400)
    Screen().setworldcoordinates(-100, -100, 100, 100)  # 200 world units -> 400px = 2x
    r = get_engine().renderer
    assert r._to_a((0, 0)) == pytest.approx((200, 200))
    assert r._to_a((50, 0)) == pytest.approx((300, 200))
    assert r._to_a((-100, -100)) == pytest.approx((0, 0))
    assert r._to_a((100, 100)) == pytest.approx((400, 400))


def test_setworldcoordinates_roundtrips_with_to_turtle():
    Screen().setup(300, 300)
    Screen().setworldcoordinates(0, 0, 30, 30)
    r = get_engine().renderer
    from arcadeturtle._coords import to_turtle
    ax, ay = r._to_a((15, 15))
    tx, ty = to_turtle(ax, ay, r.width, r.height, r.world_coords)
    assert (tx, ty) == pytest.approx((15, 15))


def test_mode_standard_clears_world_coords():
    Screen().setworldcoordinates(-50, -50, 50, 50)
    assert get_engine().renderer.world_coords is not None
    Screen().mode("standard")
    assert get_engine().renderer.world_coords is None


# ---------- bgpic ----------

def test_bgpic_default_is_nopic():
    assert Screen().bgpic() == "nopic"


def test_bgpic_loads_and_reports_name(test_png):
    Screen().bgpic(test_png)
    assert Screen().bgpic() == test_png
    assert get_engine().renderer.bg_texture is not None


def test_bgpic_nopic_clears_it(test_png):
    Screen().bgpic(test_png)
    Screen().bgpic("nopic")
    assert Screen().bgpic() == "nopic"
    assert get_engine().renderer.bg_texture is None


def test_bgpic_missing_file_raises_friendly_error():
    with pytest.raises(ArcadeTurtleError) as e:
        Screen().bgpic("this_file_does_not_exist_xyz.png")
    assert "پیدا نشد" in str(e.value)


def test_bgpic_module_level_forwards():
    assert arcadeturtle.bgpic() == "nopic"


# ---------- textinput / numinput ----------

def test_textinput_and_numinput_exist_and_are_callable_attrs():
    """اجرای واقعی دیالوگ نیاز به تعامل کاربر دارد؛ اینجا فقط مطمئن می‌شویم
    مسیر کد تا رسیدن به simpledialog درست است (import آن، نه فراخوانی مسدودکننده)."""
    import tkinter.simpledialog as simpledialog

    assert hasattr(simpledialog, "askstring")
    assert hasattr(simpledialog, "askfloat")
    assert callable(Screen().textinput)
    assert callable(Screen().numinput)
    assert callable(arcadeturtle.textinput)
    assert callable(arcadeturtle.numinput)
