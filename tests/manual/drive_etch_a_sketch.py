"""فاز ۱۰.۸ — آزمون طلایی: Etch-A-Sketch. کشیدن با موس + پاک‌کردن با کلیک راست."""

from pathlib import Path

import arcade

REPO = Path(__file__).resolve().parent.parent.parent
OUT = REPO / "tests" / "manual" / "_out_etch.png"
SCRIPT = str(REPO / "examples" / "10_etch_a_sketch.py")

state = {"step": 0}


def driver(dt):
    from arcadeturtle._engine import get_engine
    eng = get_engine()
    if eng.window is None:
        return
    state["step"] += 1
    w = eng.window

    if state["step"] == 2:
        w.on_mouse_press(300, 300, 1, 0)  # مرکز پنجره = (0,0)
    elif state["step"] == 3:
        w.on_mouse_drag(400, 400, 100, 100, 1, 0)
    elif state["step"] == 4:
        w.on_mouse_drag(200, 350, -200, -50, 1, 0)
    elif state["step"] == 5:
        w.on_mouse_release(200, 350, 1, 0)
        lines = len(eng.renderer.finished_lines)
        print("lines drawn after dragging:", lines)
        assert lines >= 2, "کشیدن باید حداقل دو پاره‌خط بسازد"
    elif state["step"] == 6:
        w.on_mouse_press(100, 100, 4, 0)  # کلیک راست (MOUSE_BUTTON_RIGHT=4) = پاک‌کن
    elif state["step"] == 7:
        assert eng.renderer.finished_lines == [], "کلیک راست باید همه‌چیز را پاک کند"
        print("clear-on-right-click OK")
    elif state["step"] == 9:
        arcade.get_image().save(OUT)
        print("saved", OUT)
        w.close()


arcade.schedule(driver, 0.2)
import runpy
runpy.run_path(SCRIPT, run_name="__main__")
