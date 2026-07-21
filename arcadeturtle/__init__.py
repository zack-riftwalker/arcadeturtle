"""ArcadeTurtle — همان API ماژول turtle، روی موتور Arcade."""

from ._errors import ArcadeTurtleError
from .api import *  # noqa: F401,F403 — API تابعی سراسری
from .api import (  # صریح، برای ابزارهای تحلیل کد
    backward, bgcolor, bk, back, clear, distance, done, down, fd, forward, goto,
    heading, hideturtle, home, ht, isdown, isvisible, left, lt, mainloop,
    pencolor, pendown, pensize, penup, pd, pos, position, pu, reset, right, rt,
    seth, setheading, setpos, setposition, setx, sety, shape, showturtle, speed,
    st, title, towards, up, width, xcor, ycor,
)
from .turtle_obj import Turtle

__version__ = "0.1.0"
