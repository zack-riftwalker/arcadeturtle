# نقاشی با کلیک موس 🖱️
# هر جا کلیک کنی، لاک‌پشت می‌رود و یک نقطه رنگی می‌گذارد.

import random

import arcadeturtle as turtle

turtle.title("هر جا خواستی کلیک کن!")
turtle.bgcolor("#fdf6e3")
turtle.speed(0)
turtle.penup()
turtle.shape("circle")

colors = ["red", "orange", "gold", "green", "dodgerblue", "purple", "hotpink"]


def paint(x, y):
    turtle.goto(x, y)
    turtle.dot(random.randint(15, 45), random.choice(colors))


turtle.onscreenclick(paint)
turtle.done()
