# شکل ترکیبی (compound) 🎨
# یک شکل چندرنگ از چند چندضلعی جدا می‌سازیم و آن را به‌عنوان شکل کرسر ثبت
# می‌کنیم — دقیقاً همان الگویی که خیلی از نقاشی‌های پیشرفته‌ی turtle استفاده
# می‌کنند.

import arcadeturtle as turtle
from arcadeturtle import Shape, Screen, Turtle

screen = Screen()
screen.bgcolor("#1a1a2e")
screen.title("شکل ترکیبی — راکت فضایی")

rocket = Shape("compound")
rocket.addcomponent(  # بدنه
    ((0, 20), (10, -10), (-10, -10)), "silver", "white",
)
rocket.addcomponent(  # نوک
    ((0, 20), (5, 5), (-5, 5)), "red", "white",
)
rocket.addcomponent(  # بال چپ
    ((-10, -10), (-18, -18), (-6, -6)), "orange", "white",
)
rocket.addcomponent(  # بال راست
    ((10, -10), (18, -18), (6, -6)), "orange", "white",
)
Screen().register_shape("rocket", rocket)

t = Turtle(shape="rocket")
t.shapesize(2, 2)
t.penup()

for i in range(5):
    t.goto(-300 + i * 150, 0)
    t.setheading(90 + i * 15)
    t.stamp()  # هر راکت را روی صفحه «مهر» می‌کنیم تا همه با هم دیده شوند

t.hideturtle()
turtle.done()
