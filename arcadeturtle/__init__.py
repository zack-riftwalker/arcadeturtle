"""ArcadeTurtle — همان API ماژول turtle، روی موتور Arcade."""

from ._errors import ArcadeTurtleError, Terminator
from .api import *  # noqa: F401,F403 — API تابعی سراسری
from .api import (  # صریح، برای ابزارهای تحلیل کد
    addshape, backward, begin_fill, bgcolor, bgpic, bk, back, bye, circle,
    clear, clearscreen, clearstamp, clearstamps, color, colormode, delay,
    distance, done, dot, down, end_fill, exitonclick, fd, fillcolor,
    filling, forward, getcanvas, get_shapepoly, getshapes, goto, heading,
    hideturtle, home, ht, isdown, isvisible, left, lt, mainloop, mode,
    pencolor, pendown, pensize, penup, pd, pos, position, pu, register_shape,
    reset, resetscreen, resizemode, right, rt, screensize, seth, setheading,
    setpos, setposition, settiltangle, setup, setworldcoordinates, setx,
    sety, shapetransform, shearfactor, teleport, tilt, tiltangle, listen,
    onclick, ondrag, onkey, onkeypress, onkeyrelease, onrelease,
    onscreenclick, ontimer, shape,
    shapesize, showturtle, speed, st, stamp, title, towards, tracer,
    turtles, turtlesize, undo, undobufferentries, setundobuffer, up, update,
    width, window_height, window_width, write, xcor, ycor,
)
from .screen import Screen, ScrolledCanvas, TurtleScreen
from .turtle_obj import Pen, RawPen, RawTurtle, Turtle
from ._shapes import Shape
from ._vec2d import Vec2D


def getscreen():
    return Screen()

__version__ = "0.1.0"
