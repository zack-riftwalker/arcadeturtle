"""کلاس Turtle — همان رابط ماژول turtle استاندارد."""

from __future__ import annotations

import math

from ._commands import InstantCmd, MoveCmd, RotateCmd
from ._engine import get_engine
from ._errors import ArcadeTurtleError, require_number, resolve_color
from ._renderer import SHAPE_POLYGONS
from ._text_fa import PERSIAN_FONT, has_persian, shape_text

_SPEED_NAMES = {"fastest": 0, "fast": 10, "normal": 6, "slow": 3, "slowest": 1}


class Turtle:
    def __init__(self, shape: str = "classic", visible: bool = True):
        eng = get_engine()
        self._id = eng.new_turtle()
        self._pen_color_raw = "black"
        self._fill_color_raw = "black"
        if shape != "classic":
            self.shape(shape)
        if not visible:
            self.hideturtle()

    # ---------- ابزار داخلی ----------

    @property
    def _eng(self):
        return get_engine()

    @property
    def _st(self):
        """state منطقی — همیشه به‌روز."""
        return self._eng.turtles[self._id].logical

    def _submit_visual(self, **changes) -> None:
        """تغییر ویژگی‌های بصری در نوبت خودش در صف اعمال می‌شود."""
        eng, tid = self._eng, self._id

        def apply():
            v = eng.turtles[tid].visual
            for k, val in changes.items():
                setattr(v, k, val)

        eng.submit(InstantCmd(tid, apply))

    def _submit_move(self, old, new) -> None:
        st = self._st
        self._eng.submit(MoveCmd(
            self._id, old, new, st.pen_down, st.pen_color, st.pen_size, st.speed
        ))

    def _submit_rotate(self, start_heading: float, delta: float) -> None:
        st = self._st
        self._eng.submit(RotateCmd(
            self._id, start_heading, (start_heading + delta) % 360.0, delta, st.speed
        ))

    def _record_fill_point(self) -> None:
        st = self._st
        if st.filling:
            st.fill_points.append((st.x, st.y))

    # ---------- حرکت ----------

    def forward(self, distance):
        require_number(distance, "forward")
        old, new = self._st.move_forward(distance)
        self._record_fill_point()
        self._submit_move(old, new)

    def backward(self, distance):
        require_number(distance, "backward")
        old, new = self._st.move_forward(-distance)
        self._record_fill_point()
        self._submit_move(old, new)

    def left(self, angle):
        require_number(angle, "left", "90")
        start = self._st.heading
        self._st.rotate(angle)
        self._submit_rotate(start, angle)

    def right(self, angle):
        require_number(angle, "right", "90")
        start = self._st.heading
        self._st.rotate(-angle)
        self._submit_rotate(start, -angle)

    def goto(self, x, y=None):
        if y is None:  # goto((x, y)) هم مجاز است، مثل turtle اصلی
            x, y = x
        require_number(x, "goto")
        require_number(y, "goto")
        old, new = self._st.goto(x, y)
        self._record_fill_point()
        self._submit_move(old, new)

    def setx(self, x):
        require_number(x, "setx")
        self.goto(x, self._st.y)

    def sety(self, y):
        require_number(y, "sety")
        self.goto(self._st.x, y)

    def home(self):
        self.goto(0, 0)
        self.setheading(0)

    def setheading(self, to_angle):
        require_number(to_angle, "setheading", "90")
        st = self._st
        # مثل turtle اصلی: چرخش از کوتاه‌ترین مسیر
        delta = (float(to_angle) - st.heading) % 360.0
        if delta > 180.0:
            delta -= 360.0
        start = st.heading
        st.set_heading(to_angle)
        self._submit_rotate(start, delta)

    # ---------- قلم ----------

    def penup(self):
        self._st.pen_down = False
        self._submit_visual(pen_down=False)

    def pendown(self):
        self._st.pen_down = True
        self._submit_visual(pen_down=True)

    def isdown(self):
        return self._st.pen_down

    def pensize(self, width=None):
        if width is None:
            return self._st.pen_size
        require_number(width, "pensize", "3")
        self._st.pen_size = width
        self._submit_visual(pen_size=width)

    def pencolor(self, *args):
        if not args:
            return self._pen_color_raw
        raw = args[0] if len(args) == 1 else tuple(args)
        rgb = resolve_color(raw)
        self._pen_color_raw = raw
        self._st.pen_color = rgb
        self._submit_visual(pen_color=rgb)

    def speed(self, speed=None):
        if speed is None:
            return self._st.speed
        if isinstance(speed, str):
            if speed not in _SPEED_NAMES:
                raise ArcadeTurtleError(
                    f"سرعت '{speed}' را نمی‌شناسم.\n"
                    "سرعت می‌تواند عدد 0 تا 10 باشد یا یکی از: "
                    "'fastest', 'fast', 'normal', 'slow', 'slowest'"
                )
            value = _SPEED_NAMES[speed]
        else:
            require_number(speed, "speed", "5")
            value = round(speed) if 0.5 < speed < 10.5 else 0
        self._st.speed = value
        self._submit_visual(speed=value)

    # ---------- کوئری‌ها (از state منطقی) ----------

    def position(self):
        return (self._st.x, self._st.y)

    def xcor(self):
        return self._st.x

    def ycor(self):
        return self._st.y

    def heading(self):
        return self._st.heading

    def towards(self, x, y=None):
        if y is None:
            if isinstance(x, Turtle):
                x, y = x.position()
            else:
                x, y = x
        return self._st.towards(x, y)

    def distance(self, x, y=None):
        if y is None:
            if isinstance(x, Turtle):
                x, y = x.position()
            else:
                x, y = x
        return self._st.distance_to(x, y)

    # ---------- ترسیم پیشرفته ----------

    def circle(self, radius, extent=None, steps=None):
        """دایره/کمان — مرکز در سمت چپ لاک‌پشت (همان معناشناسی turtle).

        با همان الگوریتم turtle استاندارد به پاره‌خط‌های ریز تبدیل می‌شود؛
        بنابراین انیمیشن و پرکردن (fill) خودبه‌خود کار می‌کنند.
        """
        require_number(radius, "circle", "50")
        if extent is None:
            extent = 360
        require_number(extent, "circle")
        if steps is None:
            frac = abs(extent) / 360
            steps = 1 + int(min(11.5 + abs(radius) / 6.0, 59.0) * frac)
        w = extent / steps
        w2 = 0.5 * w
        seg = 2.0 * radius * math.sin(math.radians(w2))
        if radius < 0:
            seg, w, w2 = -seg, -w, -w2
        self.left(w2)
        for _ in range(steps):
            self.forward(seg)
            self.left(w)
        self.left(-w2)

    def dot(self, size=None, color=None):
        st = self._st
        if size is None:
            size = max(st.pen_size + 4, st.pen_size * 2)
        else:
            require_number(size, "dot", "10")
        rgb = resolve_color(color) if color is not None else st.pen_color
        cx, cy = st.x, st.y
        r = size / 2
        points = [
            (cx + r * math.cos(math.tau * i / 24), cy + r * math.sin(math.tau * i / 24))
            for i in range(24)
        ]
        eng, tid = self._eng, self._id
        eng.submit(InstantCmd(tid, lambda: eng.renderer.add_fill(tid, points, rgb)))

    def stamp(self):
        st, eng, tid = self._st, self._eng, self._id
        sid = eng.renderer.reserve_stamp_id()
        shape, x, y = st.shape, st.x, st.y
        heading, stretch = st.heading, st.shape_size
        fill, outline = st.fill_color, st.pen_color

        eng.submit(InstantCmd(tid, lambda: eng.renderer.add_stamp(
            sid, tid, shape, x, y, heading, stretch, fill, outline)))
        return sid

    def clearstamp(self, stamp_id):
        eng = self._eng
        eng.submit(InstantCmd(self._id, lambda: eng.renderer.clear_stamp(stamp_id)))

    def clearstamps(self, n=None):
        eng, tid = self._eng, self._id
        eng.submit(InstantCmd(tid, lambda: eng.renderer.clear_stamps_of(tid, n)))

    # ---------- پرکردن ----------

    def begin_fill(self):
        st = self._st
        st.filling = True
        st.fill_points = [(st.x, st.y)]

    def end_fill(self):
        st = self._st
        if not st.filling:
            return
        st.filling = False
        points = list(st.fill_points)
        st.fill_points = []
        rgb = st.fill_color
        eng, tid = self._eng, self._id
        eng.submit(InstantCmd(tid, lambda: eng.renderer.add_fill(tid, points, rgb)))

    def filling(self):
        return self._st.filling

    def fillcolor(self, *args):
        if not args:
            return self._fill_color_raw
        raw = args[0] if len(args) == 1 else tuple(args)
        rgb = resolve_color(raw)
        self._fill_color_raw = raw
        self._st.fill_color = rgb
        self._submit_visual(fill_color=rgb)

    def color(self, *args):
        if not args:
            return (self._pen_color_raw, self._fill_color_raw)
        if len(args) == 1:
            self.pencolor(args[0])
            self.fillcolor(args[0])
        elif len(args) == 2:
            self.pencolor(args[0])
            self.fillcolor(args[1])
        else:  # سه عدد = یک رنگ RGB برای هر دو
            self.pencolor(args)
            self.fillcolor(args)

    # ---------- متن ----------

    def write(self, arg, move=False, align="left", font=("Arial", 8, "normal")):
        """نوشتن متن در محل لاک‌پشت — فارسی خودکار shaping و RTL می‌شود."""
        import arcade

        text = str(arg)
        st, eng, tid = self._st, self._eng, self._id
        x, y, rgb = st.x, st.y, st.pen_color
        font_name, font_size, *style = font if isinstance(font, (tuple, list)) else (font, 8)
        style_str = " ".join(str(s).lower() for s in style)
        if has_persian(text):
            font_name = PERSIAN_FONT
        shaped = shape_text(text)
        anchor = {"left": "left", "center": "center", "right": "right"}.get(align, "left")

        def make_text():
            ax, ay = eng.renderer._to_a((x, y))
            t = arcade.Text(
                shaped, x=ax, y=ay, color=(*rgb, 255),
                font_size=font_size, font_name=font_name,
                anchor_x=anchor, anchor_y="baseline",
                bold="bold" in style_str, italic="italic" in style_str,
            )
            eng.renderer.add_text(tid, t)

        eng.submit(InstantCmd(tid, make_text))

    # ---------- ظاهر ----------

    def shapesize(self, stretch_wid=None, stretch_len=None, outline=None):
        st = self._st
        if stretch_wid is None and stretch_len is None:
            return (*st.shape_size, 1)
        if stretch_wid is not None and stretch_len is None:
            stretch_len = stretch_wid
        if stretch_wid is None:
            stretch_wid = st.shape_size[0]
        require_number(stretch_wid, "shapesize", "2")
        require_number(stretch_len, "shapesize", "2")
        st.shape_size = (stretch_wid, stretch_len)
        self._submit_visual(shape_size=(stretch_wid, stretch_len))

    def shape(self, name=None):
        if name is None:
            return self._st.shape
        if name not in SHAPE_POLYGONS:
            available = ", ".join(sorted(SHAPE_POLYGONS))
            raise ArcadeTurtleError(
                f"شکل '{name}' وجود ندارد. 🐢\nشکل‌های موجود: {available}"
            )
        self._st.shape = name
        self._submit_visual(shape=name)

    def hideturtle(self):
        self._st.visible = False
        self._submit_visual(visible=False)

    def showturtle(self):
        self._st.visible = True
        self._submit_visual(visible=True)

    def isvisible(self):
        return self._st.visible

    # ---------- صفحه (سطح ماژول هم همین‌ها را صدا می‌زند) ----------

    def clear(self):
        """فقط نقاشی‌های همین لاک‌پشت پاک می‌شود (مثل turtle استاندارد)."""
        eng, tid = self._eng, self._id
        eng.submit(InstantCmd(tid, lambda: eng.renderer.clear_turtle(tid)))

    def reset(self):
        self.clear()
        st = self._st
        st.pen_down = True
        st.pen_size = 1
        st.pen_color = (0, 0, 0)
        st.fill_color = (0, 0, 0)
        self._pen_color_raw = "black"
        self._fill_color_raw = "black"
        old, new = st.goto(0, 0)
        st.set_heading(0)
        eng, tid = self._eng, self._id

        def snap():
            v = eng.turtles[tid].visual
            v.x, v.y = 0.0, 0.0
            v.heading = 0.0
            v.pen_down = True
            v.pen_size = 1
            v.pen_color = (0, 0, 0)
            v.fill_color = (0, 0, 0)

        eng.submit(InstantCmd(tid, snap))

    # نام‌های کوتاه (aliases) مثل turtle اصلی
    turtlesize = shapesize
    fd = forward
    bk = backward
    back = backward
    lt = left
    rt = right
    setpos = goto
    setposition = goto
    seth = setheading
    pu = penup
    up = penup
    pd = pendown
    down = pendown
    width = pensize
    pos = position
    st = showturtle
    ht = hideturtle
