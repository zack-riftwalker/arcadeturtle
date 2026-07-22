"""کلاس Screen — سینگلتون، مثل turtle.Screen() استاندارد."""

from __future__ import annotations

from ._engine import get_engine
from ._errors import (
    ArcadeTurtleError,
    get_colormode,
    require_number,
    resolve_color,
    set_colormode,
)

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
        if cmode is None:
            return get_colormode()
        set_colormode(cmode)

    def mode(self, mode=None):
        """'standard' (heading=0 شرق، پادساعتگرد) یا 'logo' (heading=0 شمال،
        ساعتگرد) یا 'world' (با setworldcoordinates). مثل stdlib، تغییر mode
        همه‌ی لاک‌پشت‌ها را ریست می‌کند."""
        eng = get_engine()
        if mode is None:
            return eng.mode_name
        mode = mode.lower()
        if mode not in ("standard", "logo", "world"):
            raise ArcadeTurtleError(
                f"mode باید یکی از 'standard', 'logo', 'world' باشد، نه {mode!r}"
            )
        eng.mode_name = mode
        if mode in ("standard", "logo"):
            eng.renderer.set_world_coords(None)
        self.reset()

    def getcanvas(self):
        raise ArcadeTurtleError(
            "getcanvas() در ArcadeTurtle معنا ندارد — رندر با Arcade/OpenGL "
            "انجام می‌شود، نه بومِ Tkinter."
        )

    def turtles(self):
        """فهرست همه لاک‌پشت‌های زنده (شبیه turtle استاندارد)."""
        return list(get_engine().turtle_objects)

    # ---------- اجرا ----------

    def delay(self, delay=None):
        """در turtle استاندارد سرعت ترسیم را کنترل می‌کند؛ اینجا فقط ذخیره
        می‌شود چون Arcade خودش با نرخ فریم ثابت رندر می‌کند — سازگاری بدون
        شکستن اسکریپت‌هایی که delay(0) یا مشابه آن را برای تنظیم سرعت صدا می‌زنند."""
        eng = get_engine()
        if delay is None:
            return getattr(eng, "pending_delay", 10)
        require_number(delay, "delay", "10")
        eng.pending_delay = delay

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

    def setworldcoordinates(self, llx, lly, urx, ury):
        """مختصات دلخواه کاربر — مستطیل (llx,lly)-(urx,ury) به کل پنجره
        کشیده می‌شود. اگر نسبت x/y آن با پنجره یکی نباشد، زاویه‌ها کج‌نما
        می‌شوند (دقیقاً همان هشداری که خودِ turtle استاندارد هم می‌دهد)."""
        for name, val in (("llx", llx), ("lly", lly), ("urx", urx), ("ury", ury)):
            require_number(val, "setworldcoordinates", "0")
        if urx <= llx or ury <= lly:
            raise ArcadeTurtleError(
                "setworldcoordinates: گوشه‌ی بالا-راست باید از پایین-چپ بزرگ‌تر باشد."
            )
        eng = get_engine()
        if eng.mode_name != "world":
            self.mode("world")  # این خودش reset را صدا می‌زند
        eng.renderer.set_world_coords((llx, lly, urx, ury))

    def bgpic(self, picname=None):
        """تصویر پس‌زمینه (PNG/GIF)، وسط‌چین با اندازه‌ی طبیعی خودش —
        picname='nopic' یعنی حذفش کن؛ بدون آرگومان یعنی نام فعلی را بگو."""
        eng = get_engine()
        r = eng.renderer
        if picname is None:
            return r.bg_name
        if picname == "nopic":
            r.clear_bgpic()
            return
        import arcade
        from pathlib import Path

        p = Path(picname)
        if not p.exists():
            raise ArcadeTurtleError(f"فایل تصویر پس‌زمینه '{picname}' پیدا نشد.")
        try:
            texture = arcade.load_texture(p)
        except Exception as e:
            raise ArcadeTurtleError(
                f"بارگذاری تصویر پس‌زمینه '{picname}' شکست خورد: {e}"
            ) from None
        r.set_bgpic(picname, texture)

    def textinput(self, title, prompt):
        """دیالوگ ساده‌ی ورودی متن (با tkinter) — اگر کاربر لغو کند None می‌دهد."""
        try:
            import tkinter.simpledialog as simpledialog
        except ImportError:
            raise ArcadeTurtleError(
                "textinput به ماژول tkinter نیاز دارد که روی این سیستم در دسترس نیست."
            ) from None
        return simpledialog.askstring(title, prompt)

    def numinput(self, title, prompt, default=None, minval=None, maxval=None):
        """دیالوگ ساده‌ی ورودی عدد (با tkinter) — اگر کاربر لغو کند None می‌دهد."""
        try:
            import tkinter.simpledialog as simpledialog
        except ImportError:
            raise ArcadeTurtleError(
                "numinput به ماژول tkinter نیاز دارد که روی این سیستم در دسترس نیست."
            ) from None
        return simpledialog.askfloat(
            title, prompt, initialvalue=default, minvalue=minval, maxvalue=maxval
        )

    def register_shape(self, name, shape=None):
        get_engine().renderer.shapes.register(name, shape)

    addshape = register_shape

    def getshapes(self):
        return get_engine().renderer.shapes.names()


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


class TurtleScreen:
    """فقط برای سازگاری import؛ در stdlib برای جاسازی turtle در یک بومِ
    Tkinter دلخواه استفاده می‌شود — چیزی که در معماری تک‌پنجره‌ی Arcade
    ما معنا ندارد. از Screen() استفاده کن."""

    def __init__(self, *args, **kwargs):
        raise ArcadeTurtleError(
            "TurtleScreen مستقیم در ArcadeTurtle پشتیبانی نمی‌شود — "
            "مخصوص جاسازی turtle در بومِ Tkinter دلخواه است.\n"
            "به‌جایش از Screen() استفاده کن."
        )


class ScrolledCanvas:
    """فقط برای سازگاری import؛ یک ویجت Tkinter است و معادلی در Arcade ندارد."""

    def __init__(self, *args, **kwargs):
        raise ArcadeTurtleError(
            "ScrolledCanvas مخصوص Tkinter است و در ArcadeTurtle پشتیبانی نمی‌شود."
        )
