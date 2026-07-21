# مارپیچ رنگی 🌀
# در هر دور، طول قدم بیشتر و رنگ عوض می‌شود.

import arcadeturtle as turtle

colors = ["red", "orange", "gold", "green", "dodgerblue", "purple"]

turtle.bgcolor("black")
turtle.speed(0)        # سرعت صفر یعنی بدون انیمیشن — فوری!
turtle.pensize(2)

for i in range(90):
    turtle.pencolor(colors[i % 6])
    turtle.forward(i * 4)
    turtle.left(59)

turtle.hideturtle()
turtle.done()
