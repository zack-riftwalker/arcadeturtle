"""Launch a user script unchanged; close its window after N seconds regardless
of activity (for scripts like the snake game whose loop never settles)."""
import runpy
import sys

import arcade

example = sys.argv[1]
seconds = float(sys.argv[2]) if len(sys.argv) > 2 else 2.0
elapsed = {"t": 0.0}


def closer(dt):
    from arcadeturtle._engine import get_engine
    eng = get_engine()
    if eng.window is None:
        return
    elapsed["t"] += dt
    if elapsed["t"] >= seconds:
        print("closing after", elapsed["t"], "seconds — no exceptions so far")
        eng.window.close()


arcade.schedule(closer, 0.1)
runpy.run_path(example, run_name="__main__")
print("clean exit")
