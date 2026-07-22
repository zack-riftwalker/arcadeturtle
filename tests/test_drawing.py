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


def test_dot_accepts_rgb_as_separate_positional_args():
    """مثل stdlib: dot(size=None, *color) — رنگ می‌تواند سه عدد جدا باشد."""
    arcadeturtle.speed(0)
    arcadeturtle.dot(20, 255, 0, 0)
    eng = get_engine()
    eng.tick(1 / 60)
    assert eng.renderer.fills[-1].color == (255, 0, 0)


def test_dot_color_only_shorthand_omits_size():
    """dot("red") بدون size — همان الگوی docstring خودِ stdlib."""
    arcadeturtle.speed(0)
    arcadeturtle.dot("red")
    eng = get_engine()
    eng.tick(1 / 60)
    assert eng.renderer.fills[-1].color == (255, 0, 0)


def test_dot_bare_call_uses_pencolor():
    arcadeturtle.speed(0)
    arcadeturtle.pencolor("green")
    arcadeturtle.dot()
    eng = get_engine()
    eng.tick(1 / 60)
    assert eng.renderer.fills[-1].color == (0, 128, 0)


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


@pytest.mark.parametrize("raw, expected", [
    ("امتیاز: 4", "4 :ﺯﺎﯿﺘﻣﺍ"),
    ("امتیاز 12 از 20", "20 ﺯﺍ 12 ﺯﺎﯿﺘﻣﺍ"),
    ("سلام Python", "Python ﻡﻼﺳ"),
    ("باختی!", "!ﯽﺘﺧﺎﺑ"),
    ("Score: 4", "Score: 4"),
])
def test_persian_shaping_locked_outputs(raw, expected):
    """خروجی‌های تأییدشده قفل می‌شوند تا رگرسیون در _text_fa زود گرفته شود.

    نکات مهم: ترتیب راست‌به‌چپ برعکس می‌شود ولی ارقام و کلمات انگلیسی
    داخل جمله باید چپ‌به‌راست و به ترتیب درست بمانند.
    """
    assert shape_text(raw) == expected


def test_clearstamps_matches_stdlib_slicing():
    """RawTurtle.clearstamps: None = همه، n >= 0 = n تای اول، n < 0 = n تای آخر.

    نکته‌ی کلیدی: n == 0 یک برش خالی است و باید هیچ مهری را پاک نکند —
    قبلاً این حالت با None اشتباه گرفته می‌شد و همه را پاک می‌کرد.
    """
    from arcadeturtle import Turtle

    t = Turtle()
    t.speed(0)
    eng = get_engine()

    def stamp_four():
        eng.renderer.stamps.clear()
        for _ in range(4):
            t.stamp()
            t.forward(20)
        eng.tick(1 / 60)

    stamp_four()
    assert len(eng.renderer.stamps) == 4
    t.clearstamps(0)
    eng.tick(1 / 60)
    assert len(eng.renderer.stamps) == 4, "n=0 نباید هیچ مهری را پاک کند"

    ids = [s.stamp_id for s in eng.renderer.stamps]
    t.clearstamps(2)  # دو تای اول
    eng.tick(1 / 60)
    assert [s.stamp_id for s in eng.renderer.stamps] == ids[2:]

    stamp_four()
    ids = [s.stamp_id for s in eng.renderer.stamps]
    t.clearstamps(-1)  # آخری
    eng.tick(1 / 60)
    assert [s.stamp_id for s in eng.renderer.stamps] == ids[:-1]

    t.clearstamps()  # همه
    eng.tick(1 / 60)
    assert eng.renderer.stamps == []


def test_turtle_clear_only_removes_own_drawings():
    """Turtle.clear() فقط نقاشی‌های خودش را پاک می‌کند؛ Screen.clear() همه را.

    این رفتار دقیق ماژول turtle استاندارد است — یک لاک‌پشت نباید با clear()
    نقاشی‌های لاک‌پشت دیگری (مثلاً تابلوی امتیاز در بازی مار) را پاک کند.
    """
    from arcadeturtle import Turtle

    a = Turtle()
    b = Turtle()
    a.speed(0)
    b.speed(0)
    a.forward(100)   # خط متعلق به a
    b.forward(50)    # خط متعلق به b
    eng = get_engine()
    eng.tick(1 / 60)
    assert len(eng.renderer.finished_lines) == 2

    a.clear()
    eng.tick(1 / 60)
    remaining = eng.renderer.finished_lines
    assert len(remaining) == 1
    assert remaining[0].turtle_id == b._id


def test_text_accumulation_warns_once(capsys):
    """write() داخل حلقه بدون clear() باید یک‌بار هشدار بدهد، نه هر بار،
    و هیچ متنی هم نباید حذف شود."""
    from arcadeturtle import _renderer

    r = _renderer.Renderer()
    n = _renderer.TEXT_WARN_THRESHOLD
    for _ in range(n + 5):
        r.add_text(0, object())  # شیء ساختگی؛ add_text فقط ذخیره می‌کند

    err = capsys.readouterr().err
    assert err.count("کند می‌شود") == 1, "هشدار باید دقیقاً یک‌بار چاپ شود"
    assert len(r.texts) == n + 5, "هیچ متنی نباید حذف شده باشد"


def test_hex_and_float_colors():
    arcadeturtle.pencolor("#ff8000")
    assert get_engine().turtles[0].logical.pen_color == (255, 128, 0)
    arcadeturtle.colormode(1.0)  # حالا لازم است، مثل turtle استاندارد
    arcadeturtle.pencolor((1.0, 0.0, 0.5))
    assert get_engine().turtles[0].logical.pen_color == (255, 0, 128)


# ---------- 10.2: Vec2D + teleport ----------

def test_position_returns_vec2d():
    from arcadeturtle._vec2d import Vec2D

    t = arcadeturtle.Turtle()
    assert isinstance(t.position(), Vec2D)
    assert isinstance(arcadeturtle.position(), Vec2D)


def test_goto_accepts_vec2d_arithmetic():
    """الگوی رایج فیزیک/بازی: goto(pos() + Vec2D(dx, dy))."""
    from arcadeturtle._vec2d import Vec2D

    t = arcadeturtle.Turtle()
    t.speed(0)
    t.goto(t.position() + Vec2D(10, 5))
    assert t.position() == pytest.approx((10, 5))


def test_teleport_moves_instantly_without_drawing_a_line():
    t = arcadeturtle.Turtle()
    t.speed(3)  # سرعت غیرصفر — teleport باید همچنان آنی باشد
    t.pendown()
    t.teleport(200, 150)
    assert t.position() == pytest.approx((200, 150))
    eng = get_engine()
    eng.tick(1 / 60)
    assert eng.turtles[t._id].visual.x == pytest.approx(200)  # بدون انیمیشن
    own_lines = [ln for ln in eng.renderer.finished_lines if ln.turtle_id == t._id]
    assert own_lines == []


def test_teleport_single_axis_keeps_other():
    t = arcadeturtle.Turtle()
    t.speed(0)
    t.goto(10, 20)
    t.teleport(x=99)
    assert t.position() == pytest.approx((99, 20))
    t.teleport(y=5)
    assert t.position() == pytest.approx((99, 5))


def test_teleport_does_not_change_heading():
    t = arcadeturtle.Turtle()
    t.speed(0)
    t.setheading(45)
    t.teleport(100, 100)
    assert t.heading() == pytest.approx(45)


def _draw_l_shape(t):
    """سه نقطه (>=۳ لازم است تا یک چندضلعیِ قابل‌پرکردن ساخته شود)."""
    t.forward(30)
    t.left(90)
    t.forward(30)


def test_teleport_without_fill_gap_splits_fill_into_two_shapes():
    t = arcadeturtle.Turtle()
    t.speed(0)
    t.begin_fill()
    _draw_l_shape(t)
    t.teleport(500, 500)
    _draw_l_shape(t)
    t.end_fill()
    eng = get_engine()
    eng.tick(1 / 60)
    own_fills = [f for f in eng.renderer.fills if f.turtle_id == t._id]
    assert len(own_fills) == 2, "بدون fill_gap باید دو شکل پرشده‌ی جدا بسازد"


def test_teleport_with_fill_gap_keeps_single_fill():
    t = arcadeturtle.Turtle()
    t.speed(0)
    t.begin_fill()
    _draw_l_shape(t)
    t.teleport(500, 500, fill_gap=True)
    _draw_l_shape(t)
    t.end_fill()
    eng = get_engine()
    eng.tick(1 / 60)
    own_fills = [f for f in eng.renderer.fills if f.turtle_id == t._id]
    assert len(own_fills) == 1, "با fill_gap=True باید یک شکل پرشده‌ی واحد بماند"
