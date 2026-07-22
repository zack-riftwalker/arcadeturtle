# Etch-A-Sketch 🖊️ — قلم را با موس بکش
# الگوی کلاسیک: t.ondrag(t.goto) یعنی «هر جا موس رفت، لاک‌پشت هم برو» —
# چون قلم پایین است، مسیر حرکت نقاشی می‌شود.

import arcadeturtle as turtle
from arcadeturtle import Screen, Turtle

screen = Screen()
screen.setup(600, 600)
screen.bgcolor("#fdf6e3")
screen.title("Etch-A-Sketch — با موس بکش، کلیک راست پاک می‌کند")

pen = Turtle(shape="circle")
pen.shapesize(0.5, 0.5)
pen.color("#073642")
pen.pensize(3)
pen.speed(0)

pen.ondrag(pen.goto)  # کشیدن با دکمه‌ی چپ موس


def clear_all():
    pen.clear()
    pen.penup()
    pen.goto(0, 0)
    pen.pendown()


screen.onclick(lambda x, y: clear_all(), btn=3)  # کلیک راست = پاک‌کردن

turtle.done()
