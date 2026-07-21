# شکل‌های پرشده + نوشتن متن فارسی ✍️
# begin_fill و end_fill داخل شکل را رنگ می‌کنند.

import arcadeturtle as turtle

turtle.bgcolor("#1e2430")
turtle.speed(0)

# ستاره پرشده طلایی
turtle.penup()
turtle.goto(-100, -60)
turtle.pendown()
turtle.color("gold", "orange")
turtle.pensize(3)
turtle.begin_fill()
for _ in range(5):
    turtle.forward(200)
    turtle.right(144)
turtle.end_fill()

# دایره پرشده سبز
turtle.penup()
turtle.goto(180, -40)
turtle.pendown()
turtle.color("lightgreen", "seagreen")
turtle.begin_fill()
turtle.circle(60)
turtle.end_fill()

# چند نقطه رنگی
turtle.penup()
for i, c in enumerate(["red", "orange", "gold", "lightgreen", "skyblue"]):
    turtle.goto(-200 + i * 100, -180)
    turtle.dot(30, c)

# متن فارسی — خودکار راست‌به‌چپ و با حروف چسبیده نوشته می‌شود
turtle.goto(0, 150)
turtle.pencolor("white")
turtle.write("سلام لاک‌پشت! 🐢 این متن فارسی است", align="center", font=("Vazirmatn", 24, "bold"))

turtle.hideturtle()
turtle.done()
