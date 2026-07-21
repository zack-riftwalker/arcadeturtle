"""Run a user example unchanged; screenshot when the command queue drains, then close.

usage: run_example_shot.py <example_path> <out_png> [extra_seconds]
"""
import runpy
import sys
from pathlib import Path

import arcade

from arcadeturtle._engine import get_engine

example = sys.argv[1]
out = Path(sys.argv[2])
extra = float(sys.argv[3]) if len(sys.argv) > 3 else 0.5

state = {"idle": 0.0, "shot": False}


def watcher(dt):
    eng = get_engine()
    if eng.window is None:
        return
    if eng.queue or eng.active_cmd is not None:
        state["idle"] = 0.0
        return
    state["idle"] += dt
    if state["idle"] >= extra and not state["shot"]:
        state["shot"] = True
        arcade.get_image().save(out)
        eng.window.close()


arcade.schedule(watcher, 1 / 30)
runpy.run_path(example, run_name="__main__")
print("saved", out)
