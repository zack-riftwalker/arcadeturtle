"""API تابعی سراسری — همان سبک `import turtle; turtle.forward(100)`.

هر تابع روی «لاک‌پشت پیش‌فرض» عمل می‌کند که با اولین استفاده ساخته می‌شود
(الگوی خود ماژول turtle استاندارد).
"""

from __future__ import annotations

from ._engine import get_engine
from ._errors import get_colormode, resolve_color, set_colormode
from .turtle_obj import Turtle

_default_turtle: Turtle | None = None


def _t() -> Turtle:
    global _default_turtle
    if _default_turtle is None:
        _default_turtle = Turtle()
    return _default_turtle


# ---------- حرکت ----------

def forward(distance): _t().forward(distance)
def backward(distance): _t().backward(distance)
def left(angle): _t().left(angle)
def right(angle): _t().right(angle)
def goto(x, y=None): _t().goto(x, y)
def setx(x): _t().setx(x)
def sety(y): _t().sety(y)
def home(): _t().home()
def setheading(to_angle): _t().setheading(to_angle)

# ---------- قلم ----------

def penup(): _t().penup()
def pendown(): _t().pendown()
def isdown(): return _t().isdown()
def pensize(width=None): return _t().pensize(width)
def pencolor(*args): return _t().pencolor(*args)
def speed(s=None): return _t().speed(s)

# ---------- ترسیم پیشرفته ----------

def circle(radius, extent=None, steps=None): _t().circle(radius, extent, steps)
def dot(size=None, color=None): _t().dot(size, color)
def stamp(): return _t().stamp()
def clearstamp(stamp_id): _t().clearstamp(stamp_id)
def clearstamps(n=None): _t().clearstamps(n)
def begin_fill(): _t().begin_fill()
def end_fill(): _t().end_fill()
def filling(): return _t().filling()
def fillcolor(*args): return _t().fillcolor(*args)
def color(*args): return _t().color(*args)
def write(arg, move=False, align="left", font=("Arial", 8, "normal")):
    _t().write(arg, move, align, font)
def shapesize(stretch_wid=None, stretch_len=None, outline=None):
    return _t().shapesize(stretch_wid, stretch_len, outline)
turtlesize = shapesize

# ---------- کوئری ----------

def position(): return _t().position()
def xcor(): return _t().xcor()
def ycor(): return _t().ycor()
def heading(): return _t().heading()
def towards(x, y=None): return _t().towards(x, y)
def distance(x, y=None): return _t().distance(x, y)

# ---------- ظاهر ----------

def shape(name=None): return _t().shape(name)
def hideturtle(): _t().hideturtle()
def showturtle(): _t().showturtle()
def isvisible(): return _t().isvisible()

# ---------- رویدادها ----------

def listen(xdummy=None, ydummy=None):
    """سازگاری با turtle — پنجره Arcade همیشه در حال گوش‌دادن است."""


def onkey(fun, key):
    get_engine().events.bind_key_press(fun, key)


def onkeypress(fun, key=None):
    get_engine().events.bind_key_press(fun, key)


def onkeyrelease(fun, key):
    get_engine().events.bind_key_release(fun, key)


def onclick(fun, btn=1, add=None):
    get_engine().events.bind_click(fun, btn)


onscreenclick = onclick


def ontimer(fun, t=0):
    get_engine().events.schedule_timer(fun, t)


def tracer(n=None, delay=None):
    eng = get_engine()
    if n is None:
        return eng.tracer_n
    eng.set_tracer(n)


def update():
    """سازگاری با turtle — Arcade خودش هر فریم صفحه را تازه می‌کند."""


# ---------- صفحه ----------

def bgcolor(*args):
    if not args:
        return get_engine().pending_bg
    raw = args[0] if len(args) == 1 else tuple(args)
    get_engine().set_bgcolor(resolve_color(raw))


def title(text):
    get_engine().set_title(str(text))


def colormode(cmode=None):
    if cmode is None:
        return get_colormode()
    set_colormode(cmode)


def clear(): _t().clear()
def reset(): _t().reset()


def done():
    get_engine().run()


def mainloop():
    done()


# ---------- نام‌های کوتاه ----------

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
ht = hideturtle
st = showturtle
