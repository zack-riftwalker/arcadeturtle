# مربع — اولین برنامه کلاسیک لاک‌پشت 🐢
# دقیقاً همان کدی که با turtle استاندارد می‌نوشتید؛ فقط import فرق دارد.

import arcadeturtle as turtle

turtle.speed(6)
turtle.pensize(3)
turtle.pencolor("royalblue")

for _ in range(4):
    turtle.forward(150)   # ۱۵۰ قدم جلو برو
    turtle.left(90)       # ۹۰ درجه بپیچ به چپ

turtle.done()             # پنجره باز بماند
