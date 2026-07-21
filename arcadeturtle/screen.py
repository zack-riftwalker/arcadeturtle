"""کلاس Screen — سینگلتون، مثل turtle.Screen() استاندارد."""

from __future__ import annotations

from ._engine import get_engine
from ._errors import ArcadeTurtleError, require_number, resolve_color

_instance = None


class _Screen:
    # ---------- پنجره ----------

    def setup(self, width=800, height=600, startx=None, starty=None):
        require_number(width, "setup", "600")
        require_number(height, "setup", "600")
        if width <= 1.0 or height <= 1.0:
            raise ArcadeTurtleError(
                "setup با عدد اعشاری (درصد صفحه‌نمایش) هنوز پشتیبانی نمی‌شود.\n"
                "اندازه را به پیکسل بده، مثل setup(600, 600)"
            )
        eng = get_engine()
        w, h = int(width), int(height)
        eng.pending_width, eng.pending_height = w, h
        eng.renderer.set_size(w, h)
        if eng.window is not None:
            eng.window.set_size(w, h)

    def title(self, text):
        get_engine().set_title(str(text))

    def bgcolor(self, *args):
        if not args:
            return get_engine().pending_bg
        raw = args[0] if len(args) == 1 else tuple(args)
        get_engine().set_bgcolor(resolve_color(raw))

    def window_width(self):
        return get_engine().pending_width

    def window_height(self):
        return get_engine().pending_height

    def screensize(self, canvwidth=None, canvheight=None, bg=None):
        return (self.window_width(), self.window_height())

    def colormode(self, cmode=None):
        # resolve_color خودش هر دو حالت 1.0 و 255 را می‌فهمد؛ برای سازگاری فقط می‌پذیرد
        if cmode is None:
            return 255

    # ---------- اجرا ----------

    def tracer(self, n=None, delay=None):
        eng = get_engine()
        if n is None:
            return eng.tracer_n
        eng.set_tracer(n)

    def update(self):
        pass  # Arcade خودش هر فریم رندر می‌کند

    def mainloop(self):
        get_engine().run()

    done = mainloop

    def bye(self):
        eng = get_engine()
        if eng.window is not None:
            eng.window.close()

    def exitonclick(self):
        self.onclick(lambda x, y: self.bye())
        self.mainloop()

    # ---------- رویدادها ----------

    def listen(self, xdummy=None, ydummy=None):
        pass

    def onkey(self, fun, key):
        get_engine().events.bind_key_press(fun, key)

    def onkeypress(self, fun, key=None):
        get_engine().events.bind_key_press(fun, key)

    def onkeyrelease(self, fun, key):
        get_engine().events.bind_key_release(fun, key)

    def onclick(self, fun, btn=1, add=None):
        get_engine().events.bind_click(fun, btn)

    onscreenclick = onclick

    def ontimer(self, fun, t=0):
        get_engine().events.schedule_timer(fun, t)

    # ---------- پاک‌سازی ----------

    def clear(self):
        get_engine().renderer.clear_all()

    clearscreen = clear

    def reset(self):
        """مثل resetscreen استاندارد: همه لاک‌پشت‌ها به حالت اولیه برمی‌گردند.

        (Screen.clear() فقط نقاشی‌ها را پاک می‌کند و لاک‌پشت‌ها را دست نمی‌زند.)
        """
        eng = get_engine()
        for t in list(eng.turtle_objects):  # کپی: reset ممکن است مجموعه را عوض کند
            t.reset()
        eng.renderer.clear_all()

    resetscreen = reset

    # ---------- پشتیبانی‌نشده‌ها با پیام تمیز ----------

    def setworldcoordinates(self, *args, **kwargs):
        raise ArcadeTurtleError(
            "setworldcoordinates هنوز در ArcadeTurtle پشتیبانی نمی‌شود.\n"
            "از مختصات معمولی (مبدأ وسط صفحه) استفاده کن."
        )

    def bgpic(self, *args, **kwargs):
        raise ArcadeTurtleError("bgpic هنوز در ArcadeTurtle پشتیبانی نمی‌شود.")

    def register_shape(self, *args, **kwargs):
        raise ArcadeTurtleError(
            "register_shape هنوز در ArcadeTurtle پشتیبانی نمی‌شود.\n"
            "از شکل‌های آماده استفاده کن: classic, turtle, square, circle, triangle, arrow"
        )

    addshape = register_shape


def Screen() -> _Screen:
    """سینگلتون — هر بار فراخوانی همان شیء را برمی‌گرداند (مثل turtle اصلی)."""
    global _instance
    if _instance is None:
        _instance = _Screen()
    return _instance


def reset_screen_singleton() -> None:
    """فقط برای تست‌ها."""
    global _instance
    _instance = None
