"""کلاس Turtle — همان رابط ماژول turtle استاندارد."""

from __future__ import annotations

from ._commands import InstantCmd, MoveCmd, RotateCmd
from ._engine import get_engine
from ._errors import ArcadeTurtleError, require_number, resolve_color
from ._renderer import SHAPE_POLYGONS

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

    # ---------- ظاهر ----------

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
        eng = self._eng
        eng.submit(InstantCmd(self._id, eng.renderer.clear_all))

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
