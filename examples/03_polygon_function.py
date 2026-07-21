# تابع با پارامتر: یک چندضلعی منظم با هر تعداد ضلع دلخواه 🔷
# همان الگویی که در آموزش توابع پایتون یاد می‌گیرید.

import arcadeturtle as turtle


def polygon(sides, length, color):
    """چندضلعی منظم با `sides` ضلع به طول `length` رسم می‌کند."""
    angle = 360 / sides
    turtle.pencolor(color)
    for _ in range(sides):
        turtle.forward(length)
        turtle.left(angle)


turtle.speed(0)
turtle.bgcolor("#101820")
turtle.pensize(3)

shapes = [
    (3, 80, "tomato"),
    (4, 80, "gold"),
    (5, 80, "lightgreen"),
    (6, 80, "skyblue"),
    (8, 80, "orchid"),
]

for i, (sides, length, color) in enumerate(shapes):
    turtle.penup()
    turtle.goto(-260 + i * 130, 0)
    turtle.pendown()
    polygon(sides, length, color)

turtle.hideturtle()
turtle.done()
