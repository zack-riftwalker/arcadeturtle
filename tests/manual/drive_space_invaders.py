"""فاز ۱۰.۸ — آزمون طلایی: فضاپیمای مهاجم. حرکت، شلیک، برخورد با مهاجم."""

from pathlib import Path

import arcade
import arcade.key

REPO = Path(__file__).resolve().parent.parent.parent
OUT = REPO / "tests" / "manual" / "_out_invaders.png"
SCRIPT = str(REPO / "examples" / "14_space_invaders.py")

ns = {"__name__": "__main__", "__file__": SCRIPT}
phase = {"n": 0, "frames": 0}


def driver(dt):
    from arcadeturtle._engine import get_engine
    eng = get_engine()
    if eng.window is None or "player" not in ns:
        return
    phase["frames"] += 1

    if phase["n"] == 0:
        print("invader count at start:", len(ns["invaders"]))
        assert len(ns["invaders"]) == 21
        eng.window.on_key_press(arcade.key.RIGHT, 0)
        phase["n"] = 1
        phase["frames"] = 0
        return

    if phase["n"] == 1:
        if phase["frames"] > 1:
            print("player moved right:", ns["player"].xcor())
            assert ns["player"].xcor() == 20
            phase["n"] = 2
            phase["frames"] = 0
        return

    if phase["n"] == 2:
        # cheat: freeze horizontal drift and put an invader right above the
        # player so the collision check is deterministic, then shoot
        ns["invader_dx"] = 0
        # نکته: گلوله فقط رو به بالا حرکت می‌کند و در player.ycor()+20 زاده
        # می‌شود؛ هدف باید بالاترِ همان نقطه باشد وگرنه گلوله هرگز بهش نمی‌رسد
        target = ns["invaders"][0]
        target.goto(ns["player"].xcor(), ns["player"].ycor() + 60)
        eng.window.on_key_press(arcade.key.SPACE, 0)
        phase["n"] = 3
        phase["frames"] = 0
        return

    if phase["n"] == 3:
        # let the game loop run a couple ticks so the bullet travels and hits
        if phase["frames"] > 3:
            print("invaders left after shot (should be 20):", len(ns["invaders"]))
            print("score (should be 10):", ns["score"])
            assert len(ns["invaders"]) == 20
            assert ns["score"] == 10
            arcade.get_image().save(OUT)
            print("saved", OUT)
            eng.window.close()
        return


arcade.schedule(driver, 0.15)
exec(compile(open(SCRIPT, encoding="utf-8").read(), SCRIPT, "exec"), ns)
