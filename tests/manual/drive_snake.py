"""Drive 08_snake_game.py headlessly via exec() with a shared globals dict so we
can read/mutate module state (food/head/score/body/game_over) while its own
mainloop() runs. Force food right in front of the head so it gets eaten (grows
+ score), then drive the snake into the wall to verify the game-over -> reset
cycle, then take a screenshot.
"""
from pathlib import Path

import arcade
import arcade.key

REPO = Path(__file__).resolve().parent.parent.parent
OUT = REPO / "tests" / "manual" / "_out_snake.png"
SCRIPT = str(REPO / "examples" / "08_snake_game.py")

ns = {"__name__": "__main__", "__file__": SCRIPT}
phase = {"n": 0, "frames": 0}


def driver(dt):
    from arcadeturtle._engine import get_engine
    eng = get_engine()
    if eng.window is None or "head" not in ns:
        return
    phase["frames"] += 1

    if phase["n"] == 0:
        eng.window.on_key_press(arcade.key.RIGHT, 0)
        ns["food"].goto(40, 0)
        phase["n"] = 1
        phase["frames"] = 0
        return

    if phase["n"] == 1:
        if phase["frames"] > 4:
            print("after eating: score =", ns["score"], "body len =", len(ns["body"]))
            assert ns["score"] == 10, f"expected score 10, got {ns['score']}"
            assert len(ns["body"]) == 1
            phase["n"] = 2
            phase["frames"] = 0
        return

    if phase["n"] == 2:
        eng.window.on_key_press(arcade.key.RIGHT, 0)
        ns["head"].goto(285, 0)
        phase["n"] = 3
        phase["frames"] = 0
        return

    if phase["n"] == 3:
        # چک زود، قبل از این‌که ریست ۹۰۰ میلی‌ثانیه‌ای game_over را برگرداند
        if phase["frames"] > 1:
            assert ns["game_over"], "expected game_over True right after wall hit"
            print("game_over flag set as expected after wall hit")
            arcade.get_image().save(OUT)
            phase["n"] = 4
            eng.window.close()
        return


arcade.schedule(driver, 0.15)
exec(compile(open(SCRIPT, encoding="utf-8").read(), SCRIPT, "exec"), ns)
print("saved", OUT)
