"""ArcadeTurtle — همان API ماژول turtle، روی موتور Arcade."""

from ._errors import ArcadeTurtleError
from .api import *  # noqa: F401,F403 — API تابعی سراسری
from .api import (  # صریح، برای ابزارهای تحلیل کد
    backward, begin_fill, bgcolor, bk, back, circle, clear, clearstamp,
    clearstamps, color, distance, done, dot, down, end_fill, fd, fillcolor,
    filling, forward, goto, heading, hideturtle, home, ht, isdown, isvisible,
    left, lt, mainloop, pencolor, pendown, pensize, penup, pd, pos, position,
    pu, reset, right, rt, seth, setheading, setpos, setposition, setx, sety,
    listen, onclick, onkey, onkeypress, onkeyrelease, onscreenclick, ontimer,
    shape, shapesize, showturtle, speed, st, stamp, title, towards, tracer,
    turtlesize, up, update, width, write, xcor, ycor,
)
from .turtle_obj import Turtle

__version__ = "0.1.0"
