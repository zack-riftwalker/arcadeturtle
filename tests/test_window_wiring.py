"""گلوی اتصال پنجره به موتور — بدون ساخت پنجره واقعی و بدون OpenGL.

این لایه نازک است ولی تا حالا هیچ تستی نداشت: فقط با اسکریپت‌های دستی
بررسی می‌شد. اینجا متدهای ArcadeTurtleWindow را روی یک نمونه‌ی ساخته‌شده
بدون __init__ صدا می‌زنیم (پس هیچ context گرافیکی لازم نیست) و تأیید می‌کنیم
هرکدام دقیقاً به متد درست موتور وصل‌اند.
"""

import pytest

from arcadeturtle._window import ArcadeTurtleWindow


class FakeEvents:
    def __init__(self):
        self.calls = []

    def handle_key_press(self, key):
        self.calls.append(("key_press", key))

    def handle_key_release(self, key):
        self.calls.append(("key_release", key))

    def handle_click(self, x, y, button):
        self.calls.append(("click", x, y, button))

    def handle_mouse_release(self, x, y, button):
        self.calls.append(("release", x, y, button))

    def handle_mouse_drag(self, x, y, buttons):
        self.calls.append(("drag", x, y, buttons))


class FakeRenderer:
    def __init__(self):
        self.drawn = []

    def draw(self, states):
        self.drawn.append(list(states))


class FakeEngine:
    def __init__(self):
        self.events = FakeEvents()
        self.renderer = FakeRenderer()
        self.ticks = []
        self._states = ["s1", "s2"]

    def tick(self, dt):
        self.ticks.append(dt)

    def visible_states(self):
        return self._states


@pytest.fixture
def win():
    """نمونه بدون __init__ — چون arcade.Window به GL context نیاز دارد."""
    w = ArcadeTurtleWindow.__new__(ArcadeTurtleWindow)
    w.engine = FakeEngine()
    return w


def test_key_press_reaches_engine(win):
    win.on_key_press(65, 0)
    assert win.engine.events.calls == [("key_press", 65)]


def test_key_release_reaches_engine(win):
    win.on_key_release(65, 0)
    assert win.engine.events.calls == [("key_release", 65)]


def test_mouse_press_passes_raw_coords_and_button(win):
    """پنجره نباید خودش مختصات را تبدیل کند — این کار EventRegistry است."""
    win.on_mouse_press(120, 340, 1, 0)
    assert win.engine.events.calls == [("click", 120, 340, 1)]


def test_on_update_forwards_delta_time(win):
    win.on_update(0.016)
    assert win.engine.ticks == [0.016]


def test_on_draw_clears_then_draws_visible_states(win):
    cleared = []
    win.clear = lambda: cleared.append(True)
    win.on_draw()
    assert cleared == [True], "صفحه باید قبل از رسم پاک شود"
    assert win.engine.renderer.drawn == [["s1", "s2"]]


def test_mouse_release_reaches_engine(win):
    win.on_mouse_release(120, 340, 1, 0)
    assert win.engine.events.calls == [("release", 120, 340, 1)]


def test_mouse_drag_passes_button_bitmask_not_raw_button(win):
    """on_mouse_drag در arcade/pyglet یک bitmask از دکمه‌های پایین می‌دهد،
    نه یک دکمه‌ی تکی — پنجره نباید این تفاوت را پنهان کند."""
    win.on_mouse_drag(120, 340, 5, 5, 0b101, 0)
    assert win.engine.events.calls == [("drag", 120, 340, 0b101)]
