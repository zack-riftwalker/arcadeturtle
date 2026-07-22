"""فاز ۱۰.۳: رجیستری شکل — چندضلعی سفارشی، compound، تصویر، resizemode، tilt،
shearfactor، shapetransform."""

import pytest

import arcadeturtle
from arcadeturtle import Screen, Shape, Turtle, api
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
    """یک PNG کوچک نامتقارن (مثلث بلندتر از عرضش) برای تست shape تصویری."""
    from PIL import Image, ImageDraw

    img = Image.new("RGBA", (20, 30), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.polygon([(10, 0), (20, 30), (0, 30)], fill=(255, 0, 0, 255))
    path = tmp_path / "ship.png"
    img.save(path)
    return str(path)


# ---------- register_shape: چندضلعی ساده ----------

def test_custom_polygon_orientation_matches_builtin_convention():
    """رگرسیون: چندضلعیِ register_shape شده باید دقیقاً همان قرارداد
    heading=0 را داشته باشد که شکل‌های آماده دارند (نوک رو به شرق در
    heading=0) — نه ۹۰ درجه اشتباه.

    این باگ واقعی بود: قبلاً فقط BUILTIN_POLYGONS چرخش (x,y)->(y,-x) را
    می‌گرفتند و چندضلعی‌های ثبت‌شده‌ی کاربر نمی‌گرفتند، چون stdlib هم این
    تبدیل را برای هر دو یکسان در _polytrafo اعمال می‌کند.
    """
    from arcadeturtle._shapes import BUILTIN_POLYGONS, transform_polygon

    custom = ((5, -3), (0, 10), (-5, -3))  # نوکِ رو به شمال، مثل مثال docstring خودِ stdlib
    at_zero = transform_polygon(custom, heading=0, stretch=(1, 1))
    nose = max(at_zero, key=lambda p: p[0])
    assert nose == pytest.approx((10.0, 0.0)), "نوک باید در heading=0 رو به شرق باشد"

    builtin_nose = max(
        transform_polygon(BUILTIN_POLYGONS["arrow"], heading=0, stretch=(1, 1)),
        key=lambda p: p[0],
    )
    assert nose == pytest.approx(builtin_nose, abs=1e-6), \
        "قرارداد جهت باید برای چندضلعی سفارشی و شکل‌های آماده یکی باشد"


def test_register_polygon_shape_and_use_it():
    Screen().register_shape("diamond", ((0, 20), (20, 0), (0, -20), (-20, 0)))
    assert "diamond" in Screen().getshapes()
    t = Turtle()
    t.shape("diamond")
    assert t.shape() == "diamond"
    assert t.get_shapepoly() == ((0.0, 20.0), (20.0, 0.0), (0.0, -20.0), (-20.0, 0.0))


def test_register_shape_rejects_too_few_points():
    with pytest.raises(ArcadeTurtleError):
        Screen().register_shape("bad", ((0, 0), (1, 1)))


def test_register_shape_rejects_garbage():
    with pytest.raises(ArcadeTurtleError):
        Screen().register_shape("bad", 12345)


def test_unknown_shape_still_raises_friendly_error():
    t = Turtle()
    with pytest.raises(ArcadeTurtleError) as e:
        t.shape("bogus")
    assert "وجود ندارد" in str(e.value)


def test_addshape_is_alias_for_register_shape():
    arcadeturtle.addshape("tri", ((0, 10), (10, -10), (-10, -10)))
    assert "tri" in arcadeturtle.getshapes()


# ---------- Shape class + compound ----------

def test_shape_rejects_invalid_type():
    with pytest.raises(ArcadeTurtleError):
        Shape("bogus_type")


def test_addcomponent_only_on_compound():
    poly = Shape("polygon", ((0, 0), (1, 1), (1, 0)))
    with pytest.raises(ArcadeTurtleError):
        poly.addcomponent(((0, 0), (1, 1), (1, 0)), "red")


def test_compound_shape_resolves_color_names_and_default_outline():
    s = Shape("compound")
    s.addcomponent(((0, 10), (10, -10), (-10, -10)), "red", "blue")
    s.addcomponent(((0, -10), (10, 10), (-10, 10)), "lime")  # بدون outline صریح
    assert s.data[0] == (((0.0, 10.0), (10.0, -10.0), (-10.0, -10.0)), (255, 0, 0), (0, 0, 255))
    assert s.data[1][1] == s.data[1][2] == (0, 255, 0)  # outline پیش‌فرض = fill


def test_register_compound_shape_and_draw_it():
    """رسم واقعی (arcade.draw_polygon_filled) به GL context زنده نیاز دارد؛
    اینجا فقط ثبت و state را بررسی می‌کنیم — رسم واقعی در
    tests/manual/verify_shapes_visual.py با اسکرین‌شات تأیید شده."""
    s = Shape("compound")
    s.addcomponent(((0, 10), (10, -10), (-10, -10)), "red")
    s.addcomponent(((0, -10), (10, 10), (-10, 10)), "blue")
    Screen().register_shape("bowtie", s)
    t = Turtle(shape="bowtie")
    assert t.get_shapepoly() is None, "compound شکل تکه‌ی واحد ندارد"
    eng = get_engine()
    eng.tick(1 / 60)  # فقط بررسی این‌که ضبط فرمان بدون خطا اجرا شود
    registered = eng.renderer.shapes.get("bowtie")
    assert registered.type == "compound"
    assert len(registered.data) == 2


# ---------- register_shape: شکل تصویری ----------

def test_register_image_shape_two_arg_form(test_png):
    Screen().register_shape("ship", test_png)
    assert "ship" in Screen().getshapes()
    t = Turtle(shape="ship")
    assert t.shape() == "ship"
    assert t.get_shapepoly() is None
    assert get_engine().renderer.shapes.get_texture("ship") is not None
    get_engine().tick(1 / 60)


def test_register_image_shape_one_arg_form_uses_original_string_as_name(test_png):
    """اسم ثبت‌شده باید دقیقاً همان رشته‌ی ورودی باشد، بدون نرمال‌سازی مسیر
    (مثل تبدیل / به \\ در ویندوز) — چون stdlib هم همین‌طور است."""
    Screen().register_shape(test_png)
    assert test_png in Screen().getshapes()


def test_register_shape_one_arg_rejects_non_image_extension():
    with pytest.raises(ArcadeTurtleError):
        Screen().register_shape("notes.txt")


def test_register_image_shape_missing_file_raises_friendly_error():
    with pytest.raises(ArcadeTurtleError) as e:
        Screen().register_shape("ghost", "does_not_exist_at_all.png")
    assert "پیدا نشد" in str(e.value)


# ---------- resizemode ----------

def test_default_resizemode_is_noresize():
    t = Turtle()
    assert t.resizemode() == "noresize"


def test_noresize_ignores_pensize():
    t = Turtle()
    t.pensize(20)
    assert t.shapesize()[:2] == (1.0, 1.0)


def test_auto_resizemode_scales_shape_with_pensize():
    t = Turtle()
    t.resizemode("auto")
    t.pensize(15)
    assert t.shapesize()[:2] == pytest.approx((3.0, 3.0))


def test_shapesize_call_switches_to_user_mode():
    t = Turtle()
    t.resizemode("auto")
    t.shapesize(2, 3)
    assert t.resizemode() == "user"
    assert t.shapesize()[:2] == (2, 3)


def test_invalid_resizemode_raises():
    t = Turtle()
    with pytest.raises(ArcadeTurtleError):
        t.resizemode("bogus")


def test_shapesize_outline_getter_setter():
    t = Turtle()
    assert t.shapesize() == (1.0, 1.0, 1.0)
    t.shapesize(1, 1, 4)
    assert t.shapesize() == (1, 1, 4)


# ---------- tilt / tiltangle / settiltangle ----------

def test_tilt_is_cumulative_and_does_not_change_heading():
    t = Turtle()
    t.setheading(30)
    t.tilt(45)
    t.tilt(45)
    assert t.tiltangle() == pytest.approx(90)
    assert t.heading() == pytest.approx(30), "tilt نباید heading را عوض کند"


def test_tiltangle_is_absolute():
    t = Turtle()
    t.tilt(45)
    t.tiltangle(10)
    assert t.tiltangle() == pytest.approx(10)


def test_settiltangle_same_as_tiltangle_setter():
    t = Turtle()
    t.settiltangle(200)
    assert t.tiltangle() == pytest.approx(200)


def test_tilt_affects_stamp_heading():
    t = Turtle()
    t.speed(0)
    t.tilt(90)
    sid = t.stamp()
    eng = get_engine()
    eng.tick(1 / 60)
    stamped = next(s for s in eng.renderer.stamps if s.stamp_id == sid)
    assert stamped.heading == pytest.approx(90)


# ---------- shearfactor / shapetransform ----------

def test_shearfactor_getter_setter():
    t = Turtle()
    assert t.shearfactor() == 0.0
    t.shearfactor(0.5)
    assert t.shearfactor() == 0.5
    assert t.resizemode() == "user"


def test_shapetransform_getter_composes_from_stretch_and_shear():
    t = Turtle()
    t.shapesize(2, 3)
    t.shearfactor(0.25)
    assert t.shapetransform() == (3, 0.25 * 3, 0.0, 2)


def test_shapetransform_setter_overrides_and_getter_reflects_it():
    t = Turtle()
    t.shapetransform(5, 0, 0, 1)
    assert t.shapetransform() == (5, 0, 0, 1)


def test_shapetransform_requires_all_four_or_none():
    t = Turtle()
    with pytest.raises(ArcadeTurtleError):
        t.shapetransform(1, 2, None, None)


@pytest.mark.parametrize("mutator", [
    lambda t: t.shapesize(2, 2),
    lambda t: t.tilt(1),
    lambda t: t.tiltangle(5),
    lambda t: t.shearfactor(0.1),
])
def test_shapetransform_override_cleared_by_composed_methods(mutator):
    t = Turtle()
    t.shapetransform(9, 9, 9, 9)
    mutator(t)
    assert t.shapetransform() != (9, 9, 9, 9)
