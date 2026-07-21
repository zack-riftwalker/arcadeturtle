"""رویدادهای کیبورد، موس و تایمر — نگاشت نام کلیدهای Turtle به Arcade."""

from __future__ import annotations

import traceback
from typing import Callable

from ._errors import ArcadeTurtleError

# نام‌های خاص Tk (که turtle استفاده می‌کند) → نام صفت در arcade.key
_SPECIAL_KEYS = {
    "up": "UP", "down": "DOWN", "left": "LEFT", "right": "RIGHT",
    "space": "SPACE", "return": "ENTER", "enter": "ENTER",
    "escape": "ESCAPE", "tab": "TAB", "backspace": "BACKSPACE",
    "delete": "DELETE", "home": "HOME", "end": "END",
    "prior": "PAGEUP", "next": "PAGEDOWN",
    "shift_l": "LSHIFT", "shift_r": "RSHIFT",
    "control_l": "LCTRL", "control_r": "RCTRL",
    "alt_l": "LALT", "alt_r": "RALT",
    "plus": "PLUS", "minus": "MINUS", "comma": "COMMA", "period": "PERIOD",
}
_SPECIAL_KEYS.update({f"f{i}": f"F{i}" for i in range(1, 13)})

# موس: شماره دکمه turtle (1=چپ 2=وسط 3=راست) → ثابت arcade
_BUTTON_MAP = {1: 1, 2: 2, 3: 4}


def resolve_key(name: str) -> int:
    import arcade.key

    if not isinstance(name, str) or not name:
        raise ArcadeTurtleError(
            f"نام کلید باید یک رشته باشد، مثل \"Up\" یا \"space\" — نه {name!r}"
        )
    low = name.lower()
    # نکته: isalpha()/isdigit() برای حروف و ارقام غیرانگلیسی هم True هستند
    # (مثلاً "۵" فارسی یا "²")، پس isascii() برای هر دو شاخه لازم است — وگرنه
    # getattr با AttributeError خام می‌ترکد به‌جای پیام مهربان پایین.
    attr = None
    if low in _SPECIAL_KEYS:
        attr = _SPECIAL_KEYS[low]
    elif len(low) == 1 and low.isascii():
        if low.isalpha():
            attr = low.upper()
        elif low.isdigit():
            attr = f"KEY_{low}"

    if attr is not None:
        key = getattr(arcade.key, attr, None)
        if key is not None:
            return key

    samples = '"Up", "Down", "Left", "Right", "space", "Return", "Escape", "a" تا "z", "0" تا "9", "F1" تا "F12"'
    raise ArcadeTurtleError(
        f"کلید '{name}' را نمی‌شناسم. ⌨️\nنمونه کلیدهای درست: {samples}"
    )


def _safe_call(fn: Callable, *args) -> None:
    """خطای داخل callback کاربر نباید کل بازی را ببندد — فقط چاپ می‌شود."""
    try:
        fn(*args)
    except Exception:
        print("⚠️ خطا داخل تابع رویداد شما رخ داد (برنامه ادامه می‌یابد):")
        traceback.print_exc()


class EventRegistry:
    def __init__(self, engine):
        self.engine = engine
        self.key_press: dict[int | None, Callable] = {}
        self.key_release: dict[int, Callable] = {}
        self.click: dict[int, Callable] = {}

    # ---------- ثبت ----------

    def bind_key_press(self, fn: Callable | None, key: str | None) -> None:
        k = None if key is None else resolve_key(key)
        if fn is None:
            self.key_press.pop(k, None)
        else:
            self.key_press[k] = fn

    def bind_key_release(self, fn: Callable | None, key: str) -> None:
        k = resolve_key(key)
        if fn is None:
            self.key_release.pop(k, None)
        else:
            self.key_release[k] = fn

    def bind_click(self, fn: Callable | None, btn: int = 1) -> None:
        b = _BUTTON_MAP.get(btn, btn)
        if fn is None:
            self.click.pop(b, None)
        else:
            self.click[b] = fn

    def schedule_timer(self, fn: Callable, t_ms: float = 0) -> None:
        import arcade

        arcade.schedule_once(lambda dt: _safe_call(fn), max(t_ms, 0) / 1000.0)

    # ---------- دریافت از پنجره ----------

    def handle_key_press(self, key: int) -> None:
        fn = self.key_press.get(key)
        if fn is not None:
            _safe_call(fn)
        any_fn = self.key_press.get(None)  # onkeypress بدون کلید = هر کلیدی
        if any_fn is not None:
            _safe_call(any_fn)

    def handle_key_release(self, key: int) -> None:
        fn = self.key_release.get(key)
        if fn is not None:
            _safe_call(fn)

    def handle_click(self, x: float, y: float, button: int) -> None:
        fn = self.click.get(button)
        if fn is not None:
            from ._coords import to_turtle

            r = self.engine.renderer
            tx, ty = to_turtle(x, y, r.width, r.height)
            _safe_call(fn, tx, ty)
