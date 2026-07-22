# نقاشی با کیبورد + دکمه‌ی undo ⏪
# جهت‌ها را بکش، و هر وقت خواستی با کلید Backspace آخرین خط را پاک کن.

import arcadeturtle as turtle
from arcadeturtle import Screen, Turtle

screen = Screen()
screen.setup(600, 600)
screen.bgcolor("black")
screen.title("نقاشی با کیبورد — جهت‌ها حرکت، Backspace = برگرد")

pen = Turtle()
pen.color("cyan")
pen.pensize(3)
pen.speed(0)
STEP = 20


def go_up():
    pen.setheading(90)
    pen.forward(STEP)


def go_down():
    pen.setheading(270)
    pen.forward(STEP)


def go_left():
    pen.setheading(180)
    pen.forward(STEP)


def go_right():
    pen.setheading(0)
    pen.forward(STEP)


def undo_last():
    pen.undo()  # هر forward/setheading یک رکورد جداگانه است -> یک Backspace کافی نیست همیشه
    pen.undo()  # setheading + forward با هم یک «قدم» بصری‌اند، هر دو را برمی‌گردانیم


screen.listen()
screen.onkeypress(go_up, "Up")
screen.onkeypress(go_down, "Down")
screen.onkeypress(go_left, "Left")
screen.onkeypress(go_right, "Right")
screen.onkeypress(undo_last, "BackSpace")

turtle.done()
