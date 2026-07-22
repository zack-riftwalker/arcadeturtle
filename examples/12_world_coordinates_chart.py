# نمودار با مختصات جهانی 📈 — setworldcoordinates
# به‌جای حساب‌کردن پیکسل، مستقیم در واحدهای خودِ داده کار می‌کنیم.

import arcadeturtle as turtle
from arcadeturtle import Screen, Turtle

screen = Screen()
screen.setup(700, 500)
screen.bgcolor("white")
screen.title("نمودار y = x² با مختصات جهانی")

# محور x از -10 تا 10، محور y از -5 تا 105 — همان بازه‌ی داده‌ی خودمان
screen.setworldcoordinates(-10, -5, 10, 105)

axis = Turtle()
axis.color("gray")
axis.pensize(1)
axis.speed(0)
axis.penup()
axis.goto(-10, 0)
axis.pendown()
axis.goto(10, 0)  # محور x
axis.penup()
axis.goto(0, -5)
axis.pendown()
axis.goto(0, 105)  # محور y

plotter = Turtle()
plotter.color("royalblue")
plotter.pensize(2)
plotter.speed(0)
plotter.hideturtle()
plotter.penup()

x = -10
plotter.goto(x, x * x)
plotter.pendown()
while x <= 10:
    plotter.goto(x, x * x)
    x += 0.5

turtle.done()
