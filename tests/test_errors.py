import sys

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


def test_no_forgot_done_warning_when_script_crashed(capsys):
    """اگر اسکریپت با خطای واقعی خودش مرده باشد، پیام done() گمراه‌کننده است."""
    from arcadeturtle._engine import _warn_if_done_forgotten
    import arcadeturtle._engine as engine_module

    arcadeturtle.forward(10)
    engine_module._engine._ran = False
    engine_module._died_with_exception = True
    try:
        _warn_if_done_forgotten()
        assert capsys.readouterr().err == ""
    finally:
        engine_module._died_with_exception = False


def test_excepthook_wrapper_sets_flag_and_chains():
    """hook باید فلگ را ست کند و hook قبلی را هم صدا بزند."""
    import arcadeturtle._engine as engine_module

    calls = []
    original = sys.excepthook
    sys.excepthook = lambda *a: calls.append(a)
    try:
        engine_module._died_with_exception = False
        engine_module._install_excepthook()
        sys.excepthook(ValueError, ValueError("boom"), None)
        assert engine_module._died_with_exception is True
        assert len(calls) == 1, "hook قبلی باید زنجیر شود، نه دور زده"
    finally:
        sys.excepthook = original
        engine_module._died_with_exception = False


def test_no_warning_after_done_or_reset(capsys):
    from arcadeturtle._engine import _warn_if_done_forgotten

    reset_engine()  # eng نداریم؛ نباید هشدار بدهد
    _warn_if_done_forgotten()
    out = capsys.readouterr()
    assert out.err == ""


def test_write_move_true_raises_instead_of_silently_ignoring():
    with pytest.raises(ArcadeTurtleError) as e:
        arcadeturtle.write("x", move=True)
    assert "پشتیبانی نمی‌شود" in str(e.value)


def test_write_without_move_is_accepted():
    arcadeturtle.write("x")            # نباید خطا بدهد
    arcadeturtle.write("x", move=False)


def test_unsupported_setup_fraction_message():
    from arcadeturtle import Screen
    with pytest.raises(ArcadeTurtleError) as e:
        Screen().setup(0.75, 0.75)
    assert "پشتیبانی نمی‌شود" in str(e.value)
