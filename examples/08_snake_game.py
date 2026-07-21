# بازی مار 🐍 — نمونه کامل با تابلوی امتیاز فارسی
# کنترل: جهت‌های کیبورد بالا/پایین/چپ/راست. نمی‌توانی مستقیم به عقب برگردی.
# این فایل معیار پایان دموی ArcadeTurtle است — همان الگوی آموزشی کلاسیک مار،
# فقط با Screen()/Turtle() به‌جای turtle خام و امتیاز فارسی.

import random

from arcadeturtle import Screen, Turtle

STEP = 20
BOUND = 280

screen = Screen()
screen.setup(600, 600)
screen.bgcolor("black")
screen.title("بازی مار 🐍 — با ArcadeTurtle")
screen.tracer(0)  # حرکت‌ها آنی‌اند؛ خودمان با ontimer صحنه را به‌روزرسانی می‌کنیم

head = Turtle(shape="square")
head.color("lightgreen")
head.penup()
head.goto(0, 0)
head.direction = "stop"

body: list[Turtle] = []

food = Turtle(shape="circle")
food.color("red")
food.penup()


def random_food_position():
    n = BOUND // STEP
    return random.randint(-n, n) * STEP, random.randint(-n, n) * STEP


food.goto(*random_food_position())

scoreboard = Turtle(visible=False)
scoreboard.penup()
scoreboard.pencolor("white")

score = 0
high_score = 0
game_over = False


def render_score():
    scoreboard.clear()
    scoreboard.goto(0, 260)
    scoreboard.write(
        f"امتیاز: {score}   رکورد: {high_score}",
        align="center", font=("Vazirmatn", 20, "bold"),
    )


render_score()


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


screen.listen()
screen.onkeypress(go_up, "Up")
screen.onkeypress(go_down, "Down")
screen.onkeypress(go_left, "Left")
screen.onkeypress(go_right, "Right")


def move_head():
    x, y = head.xcor(), head.ycor()
    if head.direction == "up":
        head.goto(x, y + STEP)
    elif head.direction == "down":
        head.goto(x, y - STEP)
    elif head.direction == "left":
        head.goto(x - STEP, y)
    elif head.direction == "right":
        head.goto(x + STEP, y)


def show_game_over_message():
    scoreboard.clear()
    scoreboard.goto(0, 0)
    scoreboard.write("باختی! 🐍", align="center", font=("Vazirmatn", 30, "bold"))


def reset_after_loss():
    global score, game_over
    for segment in body:
        segment.hideturtle()
    body.clear()
    head.goto(0, 0)
    head.direction = "stop"
    score = 0
    render_score()
    game_over = False


def game_loop():
    global score, high_score, game_over

    if game_over:
        screen.ontimer(game_loop, 120)
        return

    # ۱) بدنه حرکت می‌کند: هرکدام جای قبلیِ نفر جلویی را می‌گیرد
    for i in range(len(body) - 1, 0, -1):
        x, y = body[i - 1].position()
        body[i].goto(x, y)
    if body:
        body[0].goto(*head.position())

    # ۲) سر حرکت می‌کند
    if head.direction != "stop":
        move_head()

    # ۳) برخورد با دیوار
    if abs(head.xcor()) > BOUND or abs(head.ycor()) > BOUND:
        game_over = True
        show_game_over_message()
        screen.ontimer(reset_after_loss, 900)
        screen.update()
        screen.ontimer(game_loop, 120)
        return

    # ۴) برخورد با بدنه خودش
    for segment in body:
        if segment.distance(head) < STEP / 2:
            game_over = True
            show_game_over_message()
            screen.ontimer(reset_after_loss, 900)
            screen.update()
            screen.ontimer(game_loop, 120)
            return

    # ۵) خوردن غذا
    if head.distance(food) < STEP:
        food.goto(*random_food_position())
        new_segment = Turtle(shape="square")
        new_segment.color("darkgreen")
        new_segment.penup()
        body.append(new_segment)
        score += 10
        high_score = max(score, high_score)
        render_score()

    screen.update()
    screen.ontimer(game_loop, 120)


screen.ontimer(game_loop, 120)
screen.mainloop()
