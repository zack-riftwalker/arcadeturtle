"""خطاهای مهربان فارسی و جدول رنگ‌ها."""

from __future__ import annotations


class ArcadeTurtleError(Exception):
    """خطای آموزشی با پیام فارسی."""


# رنگ‌های رایج آموزشی (نام‌های Tk/CSS که در آموزش‌های turtle استفاده می‌شوند)
COLOR_NAMES: dict[str, tuple[int, int, int]] = {
    "black": (0, 0, 0), "white": (255, 255, 255),
    "red": (255, 0, 0), "green": (0, 128, 0), "blue": (0, 0, 255),
    "yellow": (255, 255, 0), "orange": (255, 165, 0), "purple": (128, 0, 128),
    "pink": (255, 192, 203), "brown": (165, 42, 42), "gray": (128, 128, 128),
    "grey": (128, 128, 128), "lightgray": (211, 211, 211),
    "lightgrey": (211, 211, 211), "darkgray": (169, 169, 169),
    "darkgrey": (169, 169, 169), "cyan": (0, 255, 255), "magenta": (255, 0, 255),
    "lime": (0, 255, 0), "limegreen": (50, 205, 50), "navy": (0, 0, 128),
    "teal": (0, 128, 128), "olive": (128, 128, 0), "maroon": (128, 0, 0),
    "silver": (192, 192, 192), "gold": (255, 215, 0), "violet": (238, 130, 238),
    "indigo": (75, 0, 130), "turquoise": (64, 224, 208), "salmon": (250, 128, 114),
    "coral": (255, 127, 80), "tomato": (255, 99, 71), "orchid": (218, 112, 214),
    "plum": (221, 160, 221), "khaki": (240, 230, 140), "beige": (245, 245, 220),
    "ivory": (255, 255, 240), "snow": (255, 250, 250),
    "skyblue": (135, 206, 235), "lightblue": (173, 216, 230),
    "royalblue": (65, 105, 225), "dodgerblue": (30, 144, 255),
    "steelblue": (70, 130, 180), "midnightblue": (25, 25, 112),
    "darkblue": (0, 0, 139), "darkgreen": (0, 100, 0),
    "forestgreen": (34, 139, 34), "seagreen": (46, 139, 87),
    "springgreen": (0, 255, 127), "greenyellow": (173, 255, 47),
    "darkred": (139, 0, 0), "crimson": (220, 20, 60), "firebrick": (178, 34, 34),
    "hotpink": (255, 105, 180), "deeppink": (255, 20, 147),
    "lavender": (230, 230, 250), "wheat": (245, 222, 179), "tan": (210, 180, 140),
    "chocolate": (210, 105, 30), "sienna": (160, 82, 45),
    "slategray": (112, 128, 144), "slategrey": (112, 128, 144),
    "aqua": (0, 255, 255), "fuchsia": (255, 0, 255),
    "lightgreen": (144, 238, 144), "lightyellow": (255, 255, 224),
    "lightpink": (255, 182, 193), "peachpuff": (255, 218, 185),
}


def resolve_color(value) -> tuple[int, int, int]:
    """نام رنگ / '#rrggbb' / تاپل (r,g,b) را به تاپل ۰-۲۵۵ تبدیل می‌کند."""
    if isinstance(value, str):
        name = value.strip().lower().replace(" ", "")
        if name in COLOR_NAMES:
            return COLOR_NAMES[name]
        if name.startswith("#") and len(name) == 7:
            try:
                return tuple(int(name[i:i + 2], 16) for i in (1, 3, 5))
            except ValueError:
                pass
        raise ArcadeTurtleError(
            f"رنگ '{value}' را نمی‌شناسم. 🎨\n"
            "نمونه رنگ‌های درست: red, blue, green, yellow, purple, orange\n"
            "یا کد رنگی مثل '#ff0000' یا تاپل مثل (255, 0, 0)"
        )
    if isinstance(value, (tuple, list)) and len(value) == 3:
        try:
            nums = [float(c) for c in value]
        except (TypeError, ValueError):
            raise ArcadeTurtleError(
                f"رنگ {value!r} معتبر نیست؛ سه عدد لازم است، مثل (255, 0, 0)"
            ) from None
        if all(0 <= c <= 1 for c in nums):
            # حالت colormode(1.0) خود turtle
            return tuple(round(c * 255) for c in nums)
        if all(0 <= c <= 255 for c in nums):
            return tuple(round(c) for c in nums)
        raise ArcadeTurtleError(
            f"اعداد رنگ {value!r} باید بین 0 تا 255 باشند (یا بین 0 تا 1)"
        )
    raise ArcadeTurtleError(
        f"رنگ {value!r} معتبر نیست.\n"
        "رنگ می‌تواند نام انگلیسی ('red')، کد ('#ff0000') یا تاپل (255, 0, 0) باشد."
    )


def require_number(value, func_name: str, example: str = "100"):
    """اگر value عدد نبود، خطای فارسی آموزشی می‌دهد."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ArcadeTurtleError(
            f"{func_name} یک عدد می‌خواهد، مثل {func_name}({example})\n"
            f"ولی به آن {value!r} داده شد."
        )
    return value
