"""Drive golden_snake_original.py: press 'd' to move right, force food ahead
to verify eating grows the snake and updates the score text, then drive into
the wall to verify the reset path runs without exceptions. Screenshot at end.
"""
from pathlib import Path

import arcade
import arcade.key

REPO = Path(__file__).resolve().parent.parent.parent
OUT = REPO / "tests" / "manual" / "_out_golden.png"
SCRIPT = str(REPO / "examples" / "golden_snake_original.py")

ns = {"__name__": "__main__", "__file__": SCRIPT}
phase = {"n": 0, "frames": 0}


def driver(dt):
    from arcadeturtle._engine import get_engine
    eng = get_engine()
    if eng.window is None or "head" not in ns:
        return
    phase["frames"] += 1

    if phase["n"] == 0:
        eng.window.on_key_press(arcade.key.D, 0)  # right
        ns["food"].goto(40, 0)
        phase["n"] = 1
        phase["frames"] = 0
        return

    if phase["n"] == 1:
        if phase["frames"] > 4:
            print("after eating: score =", ns["score"], "segments =", len(ns["segments"]))
            assert ns["score"] == 10
            assert len(ns["segments"]) == 1
            phase["n"] = 2
            phase["frames"] = 0
        return

    if phase["n"] == 2:
        eng.window.on_key_press(arcade.key.D, 0)
        ns["head"].goto(285, 0)
        phase["n"] = 3
        phase["frames"] = 0
        return

    if phase["n"] == 3:
        if phase["frames"] > 2:
            print("post wall-hit score:", ns["score"], "head pos:", ns["head"].position())
            assert ns["score"] == 0, "expected score reset to 0 after wall hit"
            arcade.get_image().save(OUT)
            eng.window.close()
        return


arcade.schedule(driver, 0.15)
exec(compile(open(SCRIPT, encoding="utf-8").read(), SCRIPT, "exec"), ns)
print("saved", OUT)
