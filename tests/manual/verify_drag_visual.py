"""بررسی بصری فاز ۱۰.۵: کشیدن لاک‌پشت با موس (سبک Etch-A-Sketch) روی پنجره‌ی
واقعی — نه FakeEngine. لاک‌پشت باید مسیر کشیده‌شده را نقاشی کند.
"""

from pathlib import Path

import arcade

import arcadeturtle as turtle
from arcadeturtle import Screen, Turtle

REPO = Path(__file__).resolve().parent.parent.parent
OUT = REPO / "tests" / "manual" / "_out_drag.png"

screen = Screen()
screen.setup(500, 500)
screen.bgcolor("black")
screen.tracer(0)

t = Turtle(shape="circle")
t.color("cyan")
t.penup()
t.goto(0, 0)
t.pendown()
t.ondrag(t.goto)  # الگوی کلاسیک Etch-A-Sketch: خودِ goto کال‌بک کشیدن است

state = {"step": 0}


def driver(dt):
    from arcadeturtle._engine import get_engine
    eng = get_engine()
    if eng.window is None:
        return
    state["step"] += 1
    w = eng.window

    if state["step"] == 2:
        w.on_mouse_press(250, 250, 1, 0)  # مرکز پنجره = (0,0) turtle، یعنی روی خودِ لاک‌پشت
    elif state["step"] == 3:
        w.on_mouse_drag(300, 300, 50, 50, 1, 0)
    elif state["step"] == 4:
        w.on_mouse_drag(350, 250, 50, -50, 1, 0)
    elif state["step"] == 5:
        w.on_mouse_drag(250, 200, -100, -50, 1, 0)
    elif state["step"] == 6:
        w.on_mouse_release(250, 200, 1, 0)
    elif state["step"] == 8:
        screen.update()
        arcade.get_image().save(OUT)
        print("final turtle position:", t.position())
        print("saved", OUT)
        w.close()


arcade.schedule(driver, 0.2)
screen.mainloop()
