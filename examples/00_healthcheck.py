# تست سلامت: آیا Arcade و متن فارسی روی این سیستم کار می‌کنند؟
# اگر پنجره سبز با متن فارسی خوانا دیدید، همه‌چیز آماده است.

from pathlib import Path

import arcade
import arabic_reshaper
from bidi.algorithm import get_display

FONT_PATH = Path(__file__).parent.parent / "arcadeturtle" / "assets" / "fonts" / "Vazirmatn-Regular.ttf"

arcade.load_font(str(FONT_PATH))


def shape_fa(text: str) -> str:
    return get_display(arabic_reshaper.reshape(text))


class HealthCheck(arcade.Window):
    def __init__(self):
        super().__init__(800, 600, "ArcadeTurtle Health Check")
        self.background_color = arcade.color.DARK_SPRING_GREEN
        self.text = arcade.Text(
            shape_fa("سلام! Arcade و متن فارسی کار می‌کنند 🐢"),
            x=400, y=300,
            color=arcade.color.WHITE,
            font_size=28,
            font_name="Vazirmatn",
            anchor_x="center",
        )
        self.hint = arcade.Text(
            "OpenGL OK — press ESC to close",
            x=400, y=240,
            color=arcade.color.LIGHT_GRAY,
            font_size=14,
            anchor_x="center",
        )

    def on_draw(self):
        self.clear()
        self.text.draw()
        self.hint.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.close()


if __name__ == "__main__":
    HealthCheck()
    arcade.run()
