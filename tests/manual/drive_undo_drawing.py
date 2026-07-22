"""فاز ۱۰.۸ — آزمون طلایی: نقاشی با کیبورد + undo."""

from pathlib import Path

import arcade
import arcade.key

REPO = Path(__file__).resolve().parent.parent.parent
OUT = REPO / "tests" / "manual" / "_out_undo_drawing.png"
SCRIPT = str(REPO / "examples" / "11_undo_drawing.py")

state = {"step": 0}


def driver(dt):
    from arcadeturtle._engine import get_engine
    eng = get_engine()
    if eng.window is None:
        return
    state["step"] += 1
    w = eng.window
    pen = eng.turtle_objects and next(iter(eng.turtle_objects))

    if state["step"] == 2:
        w.on_key_press(arcade.key.RIGHT, 0)
    elif state["step"] == 3:
        w.on_key_press(arcade.key.RIGHT, 0)
    elif state["step"] == 4:
        w.on_key_press(arcade.key.UP, 0)
    elif state["step"] == 5:
        pos_before = pen.position()
        print("position after 3 moves:", pos_before)
        assert pos_before == (40, 20)
    elif state["step"] == 6:
        w.on_key_press(arcade.key.BACKSPACE, 0)
    elif state["step"] == 7:
        pos_after = pen.position()
        print("position after undo (should be back to 40,0):", pos_after)
        assert pos_after == (40, 0)
    elif state["step"] == 9:
        arcade.get_image().save(OUT)
        print("saved", OUT)
        w.close()


arcade.schedule(driver, 0.2)
import runpy
runpy.run_path(SCRIPT, run_name="__main__")
