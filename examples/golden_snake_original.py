# آزمون طلایی: یک اسکریپت مار به سبک رایج آموزش‌های اینترنتی turtle
# (الگوی onkeypress + ontimer برای اجتناب از حلقه‌ی بلاک‌کننده‌ی while/sleep).
#
# تنها تغییر نسبت به نسخه‌ی اصلی همین یک خط import است — بقیه دقیقاً همان
# کدی است که با ماژول turtle استاندارد نوشته می‌شد.

import random

import arcadeturtle as turtle  # <-- تنها خط تغییر‌یافته

delay = 120  # میلی‌ثانیه بین هر فریم بازی

wn = turtle.Screen()
wn.title("Snake Game")
wn.bgcolor("black")
wn.setup(width=600, height=600)
wn.tracer(0)

head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("white")
head.penup()
head.goto(0, 0)
head.direction = "stop"

food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("red")
food.penup()
food.goto(0, 100)

segments = []

score = 0
high_score = 0

pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Score: 0  High Score: 0", align="center", font=("Courier", 24, "normal"))


def go_up():
    if head.direction != "down":
        head.direction = "up"


def go_down():
    if head.direction != "up":
        head.direction = "down"


def go_left():
    if head.direction != "right":
        head.direction = "left"


def go_right():
    if head.direction != "left":
        head.direction = "right"


def move():
    if head.direction == "up":
        y = head.ycor()
        head.sety(y + 20)
    if head.direction == "down":
        y = head.ycor()
        head.sety(y - 20)
    if head.direction == "left":
        x = head.xcor()
        head.setx(x - 20)
    if head.direction == "right":
        x = head.xcor()
        head.setx(x + 20)


wn.listen()
wn.onkeypress(go_up, "w")
wn.onkeypress(go_down, "s")
wn.onkeypress(go_left, "a")
wn.onkeypress(go_right, "d")


def game_loop():
    global score, high_score

    wn.update()

    if head.xcor() > 290 or head.xcor() < -290 or head.ycor() > 290 or head.ycor() < -290:
        head.goto(0, 0)
        head.direction = "stop"

        for segment in segments:
            segment.goto(1000, 1000)
        segments.clear()

        score = 0
        pen.clear()
        pen.write(f"Score: {score}  High Score: {high_score}",
                  align="center", font=("Courier", 24, "normal"))

    if head.distance(food) < 20:
        x = random.randint(-290, 290)
        y = random.randint(-290, 290)
        food.goto(x, y)

        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color("grey")
        new_segment.penup()
        segments.append(new_segment)

        score += 10
        if score > high_score:
            high_score = score
        pen.clear()
        pen.write(f"Score: {score}  High Score: {high_score}",
                  align="center", font=("Courier", 24, "normal"))

    for index in range(len(segments) - 1, 0, -1):
        x = segments[index - 1].xcor()
        y = segments[index - 1].ycor()
        segments[index].goto(x, y)

    if len(segments) > 0:
        x = head.xcor()
        y = head.ycor()
        segments[0].goto(x, y)

    move()

    for segment in segments:
        if segment.distance(head) < 20:
            head.goto(0, 0)
            head.direction = "stop"

            for seg in segments:
                seg.goto(1000, 1000)
            segments.clear()

            score = 0
            pen.clear()
            pen.write(f"Score: {score}  High Score: {high_score}",
                      align="center", font=("Courier", 24, "normal"))
            break

    wn.ontimer(game_loop, delay)


game_loop()
wn.mainloop()
