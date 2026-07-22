# پونگ 🏓 — دو بازیکن
# چپ: W بالا / S پایین. راست: کلید بالا / پایین. اولین نفری که به ۵ برسد می‌برد.

import arcadeturtle as turtle
from arcadeturtle import Screen, Turtle

screen = Screen()
screen.setup(700, 500)
screen.bgcolor("black")
screen.title("پونگ 🏓 — با ArcadeTurtle")
screen.tracer(0)

PADDLE_SPEED = 20
BOUND_Y = 220

left_paddle = Turtle(shape="square")
left_paddle.color("white")
left_paddle.shapesize(4, 0.5)
left_paddle.penup()
left_paddle.goto(-320, 0)

right_paddle = Turtle(shape="square")
right_paddle.color("white")
right_paddle.shapesize(4, 0.5)
right_paddle.penup()
right_paddle.goto(320, 0)

ball = Turtle(shape="circle")
ball.color("yellow")
ball.penup()
ball.goto(0, 0)
ball_dx, ball_dy = 6, 4

score_board = Turtle(visible=False)
score_board.penup()
score_board.color("white")
left_score = right_score = 0


def render_score():
    score_board.clear()
    score_board.goto(0, 210)
    score_board.write(f"{left_score}   :   {right_score}", align="center",
                      font=("Courier", 24, "normal"))


render_score()


def move_left_up():
    y = left_paddle.ycor()
    if y + PADDLE_SPEED < BOUND_Y:
        left_paddle.sety(y + PADDLE_SPEED)


def move_left_down():
    y = left_paddle.ycor()
    if y - PADDLE_SPEED > -BOUND_Y:
        left_paddle.sety(y - PADDLE_SPEED)


def move_right_up():
    y = right_paddle.ycor()
    if y + PADDLE_SPEED < BOUND_Y:
        right_paddle.sety(y + PADDLE_SPEED)


def move_right_down():
    y = right_paddle.ycor()
    if y - PADDLE_SPEED > -BOUND_Y:
        right_paddle.sety(y - PADDLE_SPEED)


screen.listen()
screen.onkeypress(move_left_up, "w")
screen.onkeypress(move_left_down, "s")
screen.onkeypress(move_right_up, "Up")
screen.onkeypress(move_right_down, "Down")


def game_loop():
    global ball_dx, ball_dy, left_score, right_score

    ball.setx(ball.xcor() + ball_dx)
    ball.sety(ball.ycor() + ball_dy)

    if ball.ycor() > 240 or ball.ycor() < -240:
        ball_dy *= -1

    # برخورد با راکت‌ها
    if (ball.xcor() > 300 and ball.xcor() < 320
            and abs(ball.ycor() - right_paddle.ycor()) < 90):
        ball_dx *= -1
    if (ball.xcor() < -300 and ball.xcor() > -320
            and abs(ball.ycor() - left_paddle.ycor()) < 90):
        ball_dx *= -1

    # گل
    if ball.xcor() > 350:
        left_score += 1
        render_score()
        ball.goto(0, 0)
        ball_dx = -6
    elif ball.xcor() < -350:
        right_score += 1
        render_score()
        ball.goto(0, 0)
        ball_dx = 6

    screen.update()
    screen.ontimer(game_loop, 30)


screen.ontimer(game_loop, 30)
screen.mainloop()
