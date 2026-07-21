"""پنجره Arcade — از دید کاربر کاملاً مخفی است."""

from __future__ import annotations

from pathlib import Path

import arcade

FONT_PATH = Path(__file__).parent / "assets" / "fonts" / "Vazirmatn-Regular.ttf"
_font_loaded = False


def ensure_font() -> None:
    global _font_loaded
    if not _font_loaded:
        arcade.load_font(str(FONT_PATH))
        _font_loaded = True


class ArcadeTurtleWindow(arcade.Window):
    def __init__(self, engine, width: int = 800, height: int = 600,
                 title: str = "ArcadeTurtle"):
        super().__init__(width, height, title)
        ensure_font()
        self.engine = engine
        self.background_color = (255, 255, 255)

    def on_draw(self):
        self.clear()
        self.engine.renderer.draw(self.engine.visible_states())

    def on_update(self, delta_time: float):
        self.engine.tick(delta_time)

    def on_key_press(self, key, modifiers):
        self.engine.events.handle_key_press(key)

    def on_key_release(self, key, modifiers):
        self.engine.events.handle_key_release(key)

    def on_mouse_press(self, x, y, button, modifiers):
        self.engine.events.handle_click(x, y, button)

    def on_mouse_release(self, x, y, button, modifiers):
        self.engine.events.handle_mouse_release(x, y, button)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.engine.events.handle_mouse_drag(x, y, buttons)
