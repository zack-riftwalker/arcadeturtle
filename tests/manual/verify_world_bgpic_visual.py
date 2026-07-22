"""بررسی بصری فاز ۱۰.۷: bgpic (تصویر پس‌زمینه) + setworldcoordinates (مختصات
دلخواه) + mode('logo'). اسکرین‌شات را دستی نگاه کن.
"""

from pathlib import Path

import arcade

import arcadeturtle as turtle
from arcadeturtle import Screen, Turtle

REPO = Path(__file__).resolve().parent.parent.parent
OUT = REPO / "tests" / "manual" / "_out_world_bgpic.png"
BG_PNG = str(REPO / "tests" / "manual" / "_test_bg.png")

screen = Screen()
screen.setup(500, 500)
screen.tracer(0)
screen.bgpic(BG_PNG)

# مختصات دلخواه: (-50,-50) تا (50,50) روی کل پنجره‌ی ۵۰۰x۵۰۰
screen.setworldcoordinates(-50, -50, 50, 50)

t = Turtle(shape="turtle")
t.color("red")
t.speed(0)
t.pensize(2)
t.penup()
t.goto(-40, -40)
t.pendown()
for _ in range(4):
    t.forward(80)
    t.left(90)

# لاک‌پشت سبز در حالت logo (رو به شمال، ساعتگرد)
tl = Turtle(shape="arrow")
tl.color("lime")
tl.penup()
tl.goto(0, 0)
tl.pendown()
tl.forward(30)  # باید رو به بالا (شمال) برود چون logo نیست هنوز -- این بعدش عوض میشه


def snap(dt):
    from arcadeturtle._engine import get_engine
    eng = get_engine()
    if eng.window is None:
        return
    screen.update()
    arcade.get_image().save(OUT)
    print("saved", OUT)
    eng.window.close()


arcade.schedule(snap, 0.3)
screen.mainloop()
