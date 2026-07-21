"""تست رجیستری رویدادها — بدون پنجره؛ رویدادها مستقیم به handler تزریق می‌شوند."""

import pytest

import arcadeturtle
from arcadeturtle import api
from arcadeturtle._engine import get_engine, reset_engine
from arcadeturtle._errors import ArcadeTurtleError
from arcadeturtle._events import resolve_key


@pytest.fixture(autouse=True)
def fresh_engine():
    reset_engine()
    api._default_turtle = None
    yield
    reset_engine()
    api._default_turtle = None


def test_resolve_special_keys():
    import arcade.key
    assert resolve_key("Up") == arcade.key.UP
    assert resolve_key("space") == arcade.key.SPACE
    assert resolve_key("Return") == arcade.key.ENTER
    assert resolve_key("a") == arcade.key.A
    assert resolve_key("7") == arcade.key.KEY_7
    assert resolve_key("F5") == arcade.key.F5


def test_unknown_key_friendly_error():
    with pytest.raises(ArcadeTurtleError) as e:
        resolve_key("Falcon")
    assert "نمی‌شناسم" in str(e.value)


@pytest.mark.parametrize("key", ["۵", "٣", "²", "ب", "ç"])
def test_non_ascii_key_gives_friendly_error_not_attributeerror(key):
    """ارقام/حروف غیرانگلیسی هم isdigit()/isalpha() را True می‌کنند؛ بدون
    محافظ isascii() اینجا AttributeError خام بیرون می‌زد."""
    with pytest.raises(ArcadeTurtleError):
        resolve_key(key)


def test_onkey_binding_and_dispatch():
    import arcade.key
    hits = []
    arcadeturtle.onkey(lambda: hits.append("up"), "Up")
    eng = get_engine()
    eng.events.handle_key_press(arcade.key.UP)
    eng.events.handle_key_press(arcade.key.DOWN)  # ثبت نشده — بی‌اثر
    assert hits == ["up"]


def test_onkey_none_unbinds():
    import arcade.key
    hits = []
    arcadeturtle.onkey(lambda: hits.append(1), "space")
    arcadeturtle.onkey(None, "space")
    get_engine().events.handle_key_press(arcade.key.SPACE)
    assert hits == []


def test_onkeypress_any_key():
    import arcade.key
    hits = []
    arcadeturtle.onkeypress(lambda: hits.append(1))  # بدون کلید = هر کلیدی
    eng = get_engine()
    eng.events.handle_key_press(arcade.key.A)
    eng.events.handle_key_press(arcade.key.Z)
    assert hits == [1, 1]


def test_click_converts_to_turtle_coords():
    got = []
    arcadeturtle.onscreenclick(lambda x, y: got.append((x, y)))
    eng = get_engine()
    eng.renderer.set_size(800, 600)
    eng.events.handle_click(400, 300, 1)  # وسط پنجره
    assert got == [(0, 0)]
    eng.events.handle_click(500, 400, 1)
    assert got[-1] == (100, 100)


def test_callback_exception_does_not_propagate(capsys):
    import arcade.key

    def bad():
        raise ValueError("boom")

    arcadeturtle.onkey(bad, "b")
    get_engine().events.handle_key_press(arcade.key.B)  # نباید exception بدهد
    out = capsys.readouterr()
    assert "خطا داخل تابع رویداد" in out.out


def test_tracer_get_set_and_instant_finish():
    arcadeturtle.tracer(0)
    assert arcadeturtle.tracer() == 0
    arcadeturtle.forward(300)
    eng = get_engine()
    eng.tick(1 / 60)
    assert eng.turtles[0].visual.x == pytest.approx(300)
    arcadeturtle.update()  # فقط نباید خطا بدهد


def test_tracer_zero_finishes_active_command():
    arcadeturtle.speed(3)
    arcadeturtle.forward(1000)
    eng = get_engine()
    eng.tick(1 / 60)  # انیمیشن شروع شده و تمام نشده
    assert eng.active_cmd is not None
    arcadeturtle.tracer(0)
    assert eng.active_cmd is None
    assert eng.turtles[0].visual.x == pytest.approx(1000)


def test_tracer_n_only_animates_every_nth_move():
    """tracer(n): فقط هر n اُمین حرکت واقعاً پخش/انیمیشن می‌شود؛ بقیه آنی."""
    t = arcadeturtle.Turtle()
    t.speed(1)  # 250 px/s — کند کافی برای مشاهده‌ی وسط انیمیشن
    arcadeturtle.tracer(3)
    for _ in range(3):
        t.forward(1000)
    eng = get_engine()

    eng.tick(1 / 60)
    assert t.position() == pytest.approx((3000, 0)), "موقعیت منطقی هیچ‌وقت نمی‌پرد"
    assert eng.active_cmd is not None, "دو حرکت اول آنی شدند، سومی الان در حال انیمیشن است"
    v_after_first_tick = eng.turtles[t._id].visual.x
    assert 2000 < v_after_first_tick < 3000, "بصری باید بین شروع و پایانِ حرکتِ سوم باشد"

    eng.tick(1 / 60)
    v_after_second_tick = eng.turtles[t._id].visual.x
    assert v_after_second_tick > v_after_first_tick, "انیمیشن باید جلوتر رفته باشد"


def test_tracer_one_is_default_and_animates_every_move():
    t = arcadeturtle.Turtle()
    t.speed(1)
    assert arcadeturtle.tracer() == 1
    t.forward(1000)
    eng = get_engine()
    eng.tick(1 / 60)
    assert eng.active_cmd is not None, "با tracer(1) همان حرکت اول هم باید انیمیشن شود"


# ---------- 10.5: کلیک/کشیدن/رهاکردن روی خودِ لاک‌پشت ----------

def test_turtle_onclick_fires_only_when_click_lands_on_it():
    eng = get_engine()
    eng.renderer.set_size(800, 600)
    t = arcadeturtle.Turtle()
    t.speed(0)
    t.penup()
    t.goto(0, 0)
    hits = []
    t.onclick(lambda x, y: hits.append((x, y)))

    eng.events.handle_click(400, 300, 1)  # مرکز پنجره = (0,0) لاک‌پشت
    assert hits == [(0, 0)]

    eng.events.handle_click(10, 10, 1)  # خیلی دور
    assert hits == [(0, 0)], "کلیک دور از لاک‌پشت نباید چیزی اضافه کند"


def test_turtle_ondrag_and_onrelease_full_sequence():
    eng = get_engine()
    eng.renderer.set_size(800, 600)
    t = arcadeturtle.Turtle()
    t.speed(0)
    t.penup()
    t.goto(0, 0)
    drags, releases = [], []
    t.ondrag(lambda x, y: drags.append((x, y)))
    t.onrelease(lambda x, y: releases.append((x, y)))

    eng.events.handle_click(400, 300, 1)   # فشردن روی لاک‌پشت -> شروع کشیدن
    eng.events.handle_mouse_drag(420, 320, 1)
    eng.events.handle_mouse_drag(450, 350, 1)
    eng.events.handle_mouse_release(450, 350, 1)

    assert drags == [(20, 20), (50, 50)]
    assert releases == [(50, 50)]


def test_ondrag_does_nothing_without_prior_press_on_turtle():
    eng = get_engine()
    eng.renderer.set_size(800, 600)
    t = arcadeturtle.Turtle()
    drags = []
    t.ondrag(lambda x, y: drags.append((x, y)))
    eng.events.handle_mouse_drag(100, 100, 1)
    assert drags == []


def test_module_level_onclick_targets_default_turtle_not_whole_screen():
    """در stdlib هم همین‌طور است: turtle.onclick سطح ماژول یعنی کلیک روی
    خودِ لاک‌پشتِ پیش‌فرض؛ برای کل صفحه باید onscreenclick صدا زد."""
    eng = get_engine()
    eng.renderer.set_size(800, 600)
    arcadeturtle.forward(0)  # فقط برای ساختن لاک‌پشت پیش‌فرض در (0,0)
    hits = []
    arcadeturtle.onclick(lambda x, y: hits.append((x, y)))
    eng.events.handle_click(700, 550, 1)  # دور از لاک‌پشت پیش‌فرض
    assert hits == [], "onclick سطح ماژول نباید مثل onscreenclick با هر کلیکی فعال شود"
    eng.events.handle_click(400, 300, 1)  # روی لاک‌پشت پیش‌فرض
    assert hits == [(0, 0)]
