# ArcadeTurtle 🐢

[فارسی 🇮🇷](README.md)

An educational library: the exact same commands as Python's standard
`turtle` module, but rendered with the modern
**[Arcade](https://api.arcade.academy/)** graphics engine — smooth
animation, a crisp modern window, and full Persian (Farsi) text support
built into `write()`.

![ArcadeTurtle sample output](docs/screenshot.png)

## Install

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install arcadeturtle
```

## Quick start

```python
import arcadeturtle as turtle

for _ in range(4):
    turtle.forward(100)
    turtle.left(90)

turtle.done()
```

That's it. Any program written for the standard `turtle` module usually
runs unchanged on ArcadeTurtle just by changing that one `import` line.

Module-level API coverage is 100% (every name in stdlib `turtle.__all__`
exists here too). To prove it, [`examples/`](examples/) contains seven
"golden tests": scripts written in the style of common internet tutorials
(a snake game, Pong, Space Invaders, Etch-A-Sketch, a compound shape, undo-
aware drawing, a world-coordinates chart) that run on ArcadeTurtle with
only the `import` line changed.

## Examples

Examples in [`examples/`](examples/), ordered simple to advanced:

| File | What it teaches |
|---|---|
| [`00_healthcheck.py`](examples/00_healthcheck.py) | Do Arcade and Persian text work on your machine? |
| [`01_square.py`](examples/01_square.py) | First moves, turns, and a loop |
| [`02_star.py`](examples/02_star.py) | Five-pointed star, background color |
| [`03_polygon_function.py`](examples/03_polygon_function.py) | Writing a function with parameters |
| [`04_color_spiral.py`](examples/04_color_spiral.py) | Nested loops, `speed(0)` |
| [`05_filled_shapes.py`](examples/05_filled_shapes.py) | `begin_fill`/`end_fill`, `dot`, Persian text |
| [`06_keyboard_drive.py`](examples/06_keyboard_drive.py) | Keyboard control (`onkeypress`) |
| [`07_click_paint.py`](examples/07_click_paint.py) | Mouse click event (`onscreenclick`) |
| [`08_snake_game.py`](examples/08_snake_game.py) | Full snake game, multiple turtles, Persian scoreboard |
| [`golden_snake_original.py`](examples/golden_snake_original.py) | A snake script in the common internet-tutorial style — runs with only the `import` changed |
| [`09_compound_shape_art.py`](examples/09_compound_shape_art.py) | `Shape("compound")`, `addcomponent`, `stamp` |
| [`10_etch_a_sketch.py`](examples/10_etch_a_sketch.py) | `Turtle.ondrag` — dragging with the mouse |
| [`11_undo_drawing.py`](examples/11_undo_drawing.py) | Keyboard drawing + `undo()` |
| [`12_world_coordinates_chart.py`](examples/12_world_coordinates_chart.py) | `setworldcoordinates` — plotting a chart in data units |
| [`13_pong.py`](examples/13_pong.py) | Two-player game, `ontimer`, collision |
| [`14_space_invaders.py`](examples/14_space_invaders.py) | `register_shape` with an image file, bullet/enemy collision |

## Compatibility with the standard `turtle` module

### ✅ Fully supported

Movement: `forward`/`fd`, `backward`/`bk`/`back`, `left`/`lt`, `right`/`rt`,
`goto`/`setpos`/`setposition`, `setx`, `sety`, `home`, `setheading`/`seth` •
Pen: `penup`/`pu`/`up`, `pendown`/`pd`/`down`, `isdown`, `pensize`/`width`,
`pencolor`, `speed` • Drawing: `circle`, `dot`, `stamp`, `clearstamp`,
`clearstamps`, `begin_fill`, `end_fill`, `filling`, `fillcolor`, `color`,
`write` (with automatic Persian support) • Appearance: `shape`,
`shapesize`/`turtlesize`, `resizemode`, `tilt`, `tiltangle`, `settiltangle`,
`shearfactor`, `shapetransform`, `get_shapepoly`, `hideturtle`/`ht`,
`showturtle`/`st`, `isvisible` • Custom shapes: `register_shape`/`addshape`
(polygon, compound shape, or PNG/GIF image file), the `Shape` class with
`addcomponent`, `getshapes` • Queries: `position`/`pos` (as a `Vec2D`),
`xcor`, `ycor`, `heading`, `towards`, `distance`, `teleport`, `degrees`,
`radians` (angle measurement unit, per-turtle) • Events: `listen`, `onkey`,
`onkeypress`, `onkeyrelease`, `onclick`/`onscreenclick`, `ontimer`,
`tracer`, `update`, `Turtle.onclick`/`ondrag`/`onrelease` (click/drag on
the turtle itself) • Undo: `undo`, `setundobuffer`, `undobufferentries`
(a separate buffer per turtle) • Utilities: `pen` (bulk get/set of pen
state), `getturtle`/`getpen`, `clone`, `begin_poly`/`end_poly`/`get_poly`
(recording a custom polygon for a later `register_shape`) • Screen:
`bgcolor`, `title`, `colormode`, `mode` (`standard`/`logo`/`world`),
`setworldcoordinates`, `bgpic`, `textinput`, `numinput`, `clear`, `reset`,
`done`/`mainloop` • Classes: `Turtle()`/`Pen()`/`RawTurtle()`/`RawPen()`
(independent instances), `Screen()` (singleton) with `setup`,
`window_width`/`window_height`, `exitonclick`, `bye`, `Vec2D`.

`clear`/`reset` are split exactly like the real turtle module:
`Turtle.clear()` only erases that turtle's own drawings, `Screen.clear()`
erases everything, and `Screen.reset()` additionally resets every turtle
to its initial state.

### 🟡 Slightly different behavior

- **`speed`**: a number 0–10 (or the names `fastest`/`fast`/`normal`/
  `slow`/`slowest`); actual pixels-per-second doesn't match stdlib turtle,
  but the relative meaning (bigger = faster, 0 = instant) is the same.
- **`colormode`**: behaves like stdlib turtle (default 255; call
  `colormode(1.0)` first for fractional colors) — but unlike stdlib
  turtle, the color mode is global rather than tied to a specific Screen
  object.
- **Image shapes rotate** — unlike stdlib turtle, which explicitly states
  "image shapes do not rotate with the turtle", this was deliberately
  reversed here: images rotate with heading, because the goal is
  supporting Space-Invaders/racing-style games that expect rotation. If
  you author your image "facing east" (nose pointing right), it lines up
  exactly with polygon shapes at heading=0.
- **`shearfactor`/`shapetransform`**: simplified relative to stdlib
  turtle's internal formula; the visual result is similar but not
  numerically identical (exact matrix "decomposition"). Scripts that call
  these independently won't notice a difference.
- **`resizemode("auto")`**: shape size is computed as `pensize / 5` — a
  documented approximation, not stdlib's exact formula.
- **`Turtle.onclick`/`ondrag`/`onrelease`**: "on the turtle" hit-testing
  uses a bounding circle, not exact point-in-polygon collision — good
  enough for ordinary interaction (like dragging with the mouse).
- **`undo`**: a separate buffer per turtle (not one shared global buffer),
  and instead of stdlib's exact reconstruction, each record restores the
  prior state directly. The same actions stdlib can undo are covered:
  movement, turning, stamps, text, `dot`, `begin_fill`/`end_fill`, and pen
  attributes. Appearance changes like `shape`/`tilt`/`resizemode` aren't
  undoable in stdlib either.
- **`bgpic`**: the background image is centered at its natural size (like
  stdlib) — it isn't stretched to fill the whole window.
- **`textinput`/`numinput`**: implemented with `tkinter.simpledialog`
  (since Arcade has no built-in input dialog); a separate window from the
  main one pops up. If tkinter isn't available on the system, they raise a
  friendly error.

### ❌ Not yet supported

Multi-window `getscreen()` (only one window at a time), and
`write(move=True)`.

These explicitly raise a friendly error rather than silently doing the
wrong thing.

Why `write(move=True)` isn't supported: moving the pen to the end of the
text requires measuring the text's width, which needs an open window —
but `write()` is usually called before `done()`, when no window exists
yet. Move the pen yourself instead:

```python
penup()
write("Hello")
goto(xcor() + 60, ycor())
pendown()
```

## How it works under the hood

Three key architectural decisions (full write-up in [ROADMAP.md](ROADMAP.md)):

1. **A single command queue**: every drawing call appends one "command" to
   a shared FIFO queue. The turtle's logical state (for `position()` and
   similar) updates immediately; playing its animation on screen happens
   over subsequent frames.
2. **Centralized coordinate conversion**: only in `_coords.py` — Turtle's
   origin is screen-center, Arcade's is the bottom-left corner.
3. **A baked line buffer**: finished lines are built once into Arcade's
   `ShapeElementList` so complex drawings (like a spiral) don't get slow.

## Running the tests

```bash
pip install -e ".[dev]"
pytest
```
