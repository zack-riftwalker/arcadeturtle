import pytest

import arcadeturtle
from arcadeturtle import api
from arcadeturtle._engine import get_engine, reset_engine
from arcadeturtle._errors import ArcadeTurtleError, resolve_color


@pytest.fixture(autouse=True)
def fresh_engine():
    reset_engine()
    api._default_turtle = None
    yield
    reset_engine()
    api._default_turtle = None


def test_resolve_color_name():
    assert resolve_color("red") == (255, 0, 0)
    assert resolve_color("RoyalBlue") == (65, 105, 225)


def test_resolve_color_hex():
    assert resolve_color("#00FF80") == (0, 255, 128)


def test_resolve_color_unknown_name_friendly():
    with pytest.raises(ArcadeTurtleError) as e:
        resolve_color("banafsh")
    assert "نمی‌شناسم" in str(e.value)


def test_resolve_color_bad_tuple_range():
    with pytest.raises(ArcadeTurtleError):
        resolve_color((300, 0, 0))


def test_unknown_shape_friendly_error():
    with pytest.raises(ArcadeTurtleError) as e:
        arcadeturtle.shape("hexagon")
    assert "وجود ندارد" in str(e.value)


def test_forgot_done_warning_fires(capsys):
    from arcadeturtle._engine import _warn_if_done_forgotten
    import arcadeturtle._engine as engine_module

    arcadeturtle.forward(10)  # یک لاک‌پشت ساخته می‌شود ولی done() صدا زده نمی‌شود
    engine_module._engine._ran = False  # شبیه‌سازی خروج بدون done()
    _warn_if_done_forgotten()
    out = capsys.readouterr()
    assert "done()" in out.err
    assert "فراموش کرده‌ای" in out.err


def test_no_warning_after_done_or_reset(capsys):
    from arcadeturtle._engine import _warn_if_done_forgotten

    reset_engine()  # eng نداریم؛ نباید هشدار بدهد
    _warn_if_done_forgotten()
    out = capsys.readouterr()
    assert out.err == ""


def test_unsupported_setup_fraction_message():
    from arcadeturtle import Screen
    with pytest.raises(ArcadeTurtleError) as e:
        Screen().setup(0.75, 0.75)
    assert "پشتیبانی نمی‌شود" in str(e.value)
