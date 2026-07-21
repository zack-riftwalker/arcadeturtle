"""بررسی بصری فاز ۱۰.۳: شکل تصویری (رندر + جهت چرخش)، شکل ترکیبی (compound)،
tilt، و resizemode="auto". اسکرین‌شات را دستی نگاه کن.
"""

from pathlib import Path

import arcade

import arcadeturtle as turtle
from arcadeturtle import Shape, Screen, Turtle

REPO = Path(__file__).resolve().parent.parent.parent
OUT = REPO / "tests" / "manual" / "_out_shapes.png"
SHIP_PNG = str(REPO / "tests" / "manual" / "_test_ship.png")

screen = Screen()
screen.setup(700, 700)
screen.bgcolor("#101820")
screen.tracer(0)

screen.register_shape("ship", SHIP_PNG)

# چهار جهت — نوک مثلث باید هر بار رو به جهت heading باشد
headings = [0, 90, 180, 270]
positions = [(-200, 200), (200, 200), (200, -200), (-200, -200)]
for h, (x, y) in zip(headings, positions):
    t = Turtle(shape="ship")
    t.penup()
    t.goto(x, y)
    t.setheading(h)

# شکل ترکیبی: پروانه دو رنگ
bow = Shape("compound")
bow.addcomponent(((0, 25), (25, -25), (-25, -25)), "orange", "white")
bow.addcomponent(((0, -25), (25, 25), (-25, 25)), "purple", "white")
screen.register_shape("bowtie", bow)
tb = Turtle(shape="bowtie")
tb.penup()
tb.goto(0, 0)

# tilt: کرسر classic که چرخش ظاهری دارد ولی heading (جهت حرکت) صفر می‌ماند
tt = Turtle(shape="turtle")
tt.color("lightgreen")
tt.penup()
tt.goto(0, 250)
tt.tilt(90)

# resizemode="auto": شکل با ضخامت قلم بزرگ می‌شود
ta = Turtle(shape="classic")
ta.color("yellow")
ta.penup()
ta.goto(0, -300)
ta.resizemode("auto")
ta.pensize(25)

def snap(dt):
    from arcadeturtle._engine import get_engine
    eng = get_engine()
    if eng.window is None:
        return
    arcade.get_image().save(OUT)
    print("saved", OUT)
    eng.window.close()


arcade.schedule(snap, 0.3)
screen.mainloop()
