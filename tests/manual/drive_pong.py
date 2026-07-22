"""فاز ۱۰.۸ — آزمون طلایی: پونگ. حرکت راکت، برخورد با دیوار بالا/پایین، گل."""

from pathlib import Path

import arcade
import arcade.key

REPO = Path(__file__).resolve().parent.parent.parent
OUT = REPO / "tests" / "manual" / "_out_pong.png"
SCRIPT = str(REPO / "examples" / "13_pong.py")

ns = {"__name__": "__main__", "__file__": SCRIPT}
phase = {"n": 0, "frames": 0}


def driver(dt):
    from arcadeturtle._engine import get_engine
    eng = get_engine()
    if eng.window is None or "left_paddle" not in ns:
        return
    phase["frames"] += 1

    if phase["n"] == 0:
        eng.window.on_key_press(arcade.key.W, 0)
        eng.window.on_key_press(arcade.key.W, 0)
        phase["n"] = 1
        phase["frames"] = 0
        return

    if phase["n"] == 1:
        if phase["frames"] > 2:
            y = ns["left_paddle"].ycor()
            print("left paddle moved up via 'w':", y)
            assert y == 40
            phase["n"] = 2
            phase["frames"] = 0
        return

    if phase["n"] == 2:
        # force the ball toward the top wall to check bounce
        ns["ball"].sety(238)
        globals_dy_before = ns["ball_dy"]
        phase["n"] = 3
        phase["frames"] = 0
        return

    if phase["n"] == 3:
        if phase["frames"] > 1:
            print("ball_dy after hitting top wall (should have flipped sign):", ns["ball_dy"])
            assert ns["ball_dy"] < 0
            phase["n"] = 4
            phase["frames"] = 0
        return

    if phase["n"] == 4:
        # force a goal: put ball past the right edge
        ns["ball"].goto(360, 0)
        phase["n"] = 5
        phase["frames"] = 0
        return

    if phase["n"] == 5:
        if phase["frames"] > 1:
            print("left_score after right-edge goal (should be 1):", ns["left_score"])
            assert ns["left_score"] == 1
            assert abs(ns["ball"].xcor()) < 350, "گل باید توپ را از لبه برگرداند به وسط"
            arcade.get_image().save(OUT)
            print("saved", OUT)
            eng.window.close()
        return


arcade.schedule(driver, 0.15)
exec(compile(open(SCRIPT, encoding="utf-8").read(), SCRIPT, "exec"), ns)
