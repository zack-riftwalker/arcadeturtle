# کنترل لاک‌پشت با کیبورد 🎮
# با جهت‌های کیبورد لاک‌پشت را حرکت بده — پشت سرش خط می‌کشد!

import arcadeturtle as turtle

turtle.title("با جهت‌های کیبورد حرکت بده!")
turtle.bgcolor("#0f1626")
turtle.pencolor("cyan")
turtle.pensize(3)
turtle.shape("turtle")
turtle.speed(0)


def go_up():
    turtle.setheading(90)
    turtle.forward(20)


def go_down():
    turtle.setheading(270)
    turtle.forward(20)


def go_left():
    turtle.setheading(180)
    turtle.forward(20)


def go_right():
    turtle.setheading(0)
    turtle.forward(20)


def clear_screen():
    turtle.clear()


turtle.listen()
turtle.onkeypress(go_up, "Up")
turtle.onkeypress(go_down, "Down")
turtle.onkeypress(go_left, "Left")
turtle.onkeypress(go_right, "Right")
turtle.onkeypress(clear_screen, "space")   # space = پاک‌کردن صفحه

turtle.done()
