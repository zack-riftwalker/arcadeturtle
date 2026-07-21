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
