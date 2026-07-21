"""فاز ۱۰.۴: undo با بافر جداگانه برای هر لاک‌پشت."""

import pytest

import arcadeturtle
from arcadeturtle import Turtle, api
from arcadeturtle._engine import get_engine, reset_engine
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


def test_undo_move_and_rotate_matches_stdlib_docstring_pattern():
    """دقیقاً مثل مثال docstring خودِ stdlib: ۴ بار (fd+lt)، بعد ۸ بار undo."""
    t = Turtle()
    t.speed(0)
    for _ in range(4):
        t.forward(50)
        t.left(80)
    eng = get_engine()
    eng.tick(1 / 60)
    assert t.position() != pytest.approx((0, 0))

    for _ in range(8):
        t.undo()
    eng.tick(1 / 60)

    assert t.position() == pytest.approx((0, 0))
    assert t.heading() == pytest.approx(0)
    own_lines = [ln for ln in eng.renderer.finished_lines if ln.turtle_id == t._id]
    assert own_lines == []


def test_undo_forward_with_pen_up_does_not_touch_lines():
    t = Turtle()
    t.speed(0)
    t.penup()
    t.forward(100)
    eng = get_engine()
    eng.tick(1 / 60)
    t.undo()
    eng.tick(1 / 60)
    assert t.position() == pytest.approx((0, 0))


def test_undo_pencolor_restores_previous_raw_and_resolved_value():
    t = Turtle()
    t.pencolor("red")
    t.pencolor("blue")
    t.undo()
    assert t.pencolor() == "red"


def test_undo_fillcolor_restores_previous():
    t = Turtle()
    t.fillcolor("green")
    t.fillcolor("yellow")
    t.undo()
    assert t.fillcolor() == "green"


def test_undo_pensize_restores_previous():
    t = Turtle()
    t.pensize(5)
    t.undo()
    assert t.pensize() == 1


def test_undo_penup_pendown():
    t = Turtle()
    assert t.isdown()
    t.penup()
    t.undo()
    assert t.isdown()
    t.penup()
    assert not t.isdown()
    t.pendown()
    t.undo()
    assert not t.isdown()


def test_undo_stamp_removes_it():
    t = Turtle()
    t.speed(0)
    t.stamp()
    eng = get_engine()
    eng.tick(1 / 60)
    assert len(eng.renderer.stamps) == 1
    t.undo()
    eng.tick(1 / 60)
    assert len(eng.renderer.stamps) == 0


def test_undo_dot_removes_it():
    t = Turtle()
    t.speed(0)
    t.dot(20)
    eng = get_engine()
    eng.tick(1 / 60)
    own_fills = [f for f in eng.renderer.fills if f.turtle_id == t._id]
    assert len(own_fills) == 1
    t.undo()
    eng.tick(1 / 60)
    own_fills = [f for f in eng.renderer.fills if f.turtle_id == t._id]
    assert own_fills == []


def test_undo_write_removes_it():
    t = Turtle()
    t.write("hi")
    eng = get_engine()
    eng.tick(1 / 60)
    own_texts = [x for x in eng.renderer.texts if x.turtle_id == t._id]
    assert len(own_texts) == 1
    t.undo()
    eng.tick(1 / 60)
    own_texts = [x for x in eng.renderer.texts if x.turtle_id == t._id]
    assert own_texts == []


def test_undo_end_fill_reopens_the_same_polygon_in_progress():
    t = Turtle()
    t.speed(0)
    t.begin_fill()
    t.forward(30)
    t.left(90)
    t.forward(30)
    t.end_fill()
    eng = get_engine()
    eng.tick(1 / 60)
    own_fills = [f for f in eng.renderer.fills if f.turtle_id == t._id]
    assert len(own_fills) == 1

    t.undo()  # undo end_fill
    eng.tick(1 / 60)
    own_fills = [f for f in eng.renderer.fills if f.turtle_id == t._id]
    assert own_fills == [], "پرکردنِ پخته‌شده باید پاک شود"
    assert t.filling() is True, "باید دوباره در حالت پرکردن باشد"


def test_undo_begin_fill_cancels_it():
    t = Turtle()
    t.begin_fill()
    assert t.filling()
    t.undo()
    assert not t.filling()


def test_undo_does_not_disturb_other_turtles_pending_commands():
    """undo روی یک لاک‌پشت نباید فرمان‌های در صفِ لاک‌پشت دیگر را دست بزند."""
    a, b = Turtle(), Turtle()
    a.speed(0)
    b.speed(3)  # فرمان b در صف می‌ماند، هنوز پردازش نشده

    a.forward(50)
    b.forward(200)
    a.undo()  # قبل از هر tick

    assert a.position() == pytest.approx((0, 0))
    assert b.position() == pytest.approx((200, 0)), "موقعیت منطقی b نباید دست بخورد"

    eng = get_engine()
    while eng.queue or eng.active_cmd is not None:
        eng.tick(1 / 60)
    assert b.position() == pytest.approx((200, 0))
    assert a.position() == pytest.approx((0, 0))


def test_undo_on_empty_stack_is_a_silent_noop():
    t = Turtle()
    t.undo()  # نباید خطا بدهد
    assert t.position() == pytest.approx((0, 0))


def test_setundobuffer_installs_fresh_empty_buffer():
    t = Turtle()
    t.speed(0)
    t.forward(10)
    t.forward(10)
    assert t.undobufferentries() == 2

    t.setundobuffer(5)
    assert t.undobufferentries() == 0, "setundobuffer باید بافر تازه و خالی نصب کند"

    for _ in range(3):
        t.forward(10)
    assert t.undobufferentries() == 3


def test_undo_buffer_caps_at_configured_size():
    t = Turtle()
    t.speed(0)
    t.setundobuffer(2)
    for _ in range(5):
        t.forward(10)
    assert t.undobufferentries() == 2


def test_setundobuffer_none_disables_undo():
    t = Turtle()
    t.setundobuffer(None)
    t.forward(10)
    assert t.undobufferentries() == 0
    t.undo()  # نباید خطا بدهد
    assert t.position() == pytest.approx((10, 0)), "بدون بافر، undo کاری نمی‌کند"
