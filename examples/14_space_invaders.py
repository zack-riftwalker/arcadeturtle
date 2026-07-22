# فضاپیمای مهاجم 👾 — چپ/راست حرکت، Space شلیک
# سفینه‌ی بازیکن یک shape تصویریِ ساخته‌شده در لحظه است (register_shape با
# فایل PNG) — همان چیزی که آموزش‌های واقعی Space Invaders استفاده می‌کنند.

import tempfile
from pathlib import Path

import arcadeturtle as turtle
from arcadeturtle import Screen, Turtle

# --- ساخت یک تصویر سفینه‌ی ساده در لحظه (بدون فایل همراه کتابخانه) ---
_SHIP_PNG = Path(tempfile.gettempdir()) / "arcadeturtle_demo_ship.png"
if not _SHIP_PNG.exists():
    from PIL import Image, ImageDraw
    img = Image.new("RGBA", (36, 24), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.polygon([(36, 12), (0, 0), (8, 12), (0, 24)], fill=(80, 220, 120, 255))
    img.save(_SHIP_PNG)

screen = Screen()
screen.setup(600, 600)
screen.bgcolor("black")
screen.title("فضاپیمای مهاجم 👾")
screen.tracer(0)
screen.register_shape("ship", str(_SHIP_PNG))

player = Turtle(shape="ship")
player.penup()
player.goto(0, -260)
player.speed(0)

bullets = []
invaders = []

for row in range(3):
    for col in range(7):
        inv = Turtle(shape="triangle")
        inv.color("tomato")
        inv.penup()
        inv.setheading(270)
        inv.goto(-240 + col * 80, 220 - row * 60)
        invaders.append(inv)

invader_dx = 2

score_board = Turtle(visible=False)
score_board.penup()
score_board.color("white")
score = 0


def render_score():
    score_board.clear()
    score_board.goto(0, 270)
    score_board.write(f"امتیاز: {score}", align="center", font=("Vazirmatn", 18, "bold"))


render_score()


def move_left():
    x = player.xcor()
    if x > -280:
        player.setx(x - 20)


def move_right():
    x = player.xcor()
    if x < 280:
        player.setx(x + 20)


def shoot():
    b = Turtle(shape="circle")
    b.color("yellow")
    b.shapesize(0.4, 0.4)
    b.penup()
    b.goto(player.xcor(), player.ycor() + 20)
    bullets.append(b)


screen.listen()
screen.onkeypress(move_left, "Left")
screen.onkeypress(move_right, "Right")
screen.onkeypress(shoot, "space")


def game_loop():
    global invader_dx, score

    edge_hit = False
    for inv in invaders:
        inv.setx(inv.xcor() + invader_dx)
        if inv.xcor() > 280 or inv.xcor() < -280:
            edge_hit = True
    if edge_hit:
        invader_dx *= -1
        for inv in invaders:
            inv.sety(inv.ycor() - 15)

    for b in list(bullets):
        b.sety(b.ycor() + 15)
        if b.ycor() > 300:
            b.hideturtle()
            bullets.remove(b)
            continue
        for inv in list(invaders):
            if b.distance(inv) < 20:
                inv.hideturtle()
                invaders.remove(inv)
                b.hideturtle()
                if b in bullets:
                    bullets.remove(b)
                score += 10
                render_score()
                break

    screen.update()
    screen.ontimer(game_loop, 30)


screen.ontimer(game_loop, 30)
screen.mainloop()
