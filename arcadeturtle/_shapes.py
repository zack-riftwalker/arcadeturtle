"""شکل‌های کرسر: چندضلعی ساده، ترکیبی (compound)، یا تصویر (GIF/PNG).

شکل‌های آماده + هرچه کاربر با register_shape ثبت کند، هر دو در همین رجیستری
جای می‌گیرند — دقیقاً مثل خودِ turtle استاندارد که هر دو را در یک دیکشنری
نگه می‌دارد.
"""

from __future__ import annotations

import math
from pathlib import Path

from ._coords import heading_to_arcade_angle
from ._errors import ArcadeTurtleError, resolve_color

Point = tuple[float, float]

IMAGE_SUFFIXES = (".gif", ".png")


def _east(points: tuple[tuple[float, float], ...]) -> tuple[tuple[float, float], ...]:
    """چندضلعی‌های stdlib turtle رو به شمال تعریف شده‌اند؛ اینجا با
    (x, y) -> (y, -x) رو به شرق ذخیره می‌شوند تا heading=0 درست باشد."""
    return tuple((y, -x) for x, y in points)


BUILTIN_POLYGONS: dict[str, tuple[Point, ...]] = {
    "arrow": _east(((-10, 0), (10, 0), (0, 10))),
    "turtle": _east((
        (0, 16), (-2, 14), (-1, 10), (-4, 7), (-7, 9), (-9, 8), (-6, 5),
        (-7, 1), (-5, -3), (-8, -6), (-6, -8), (-4, -5), (0, -7), (4, -5),
        (6, -8), (8, -6), (5, -3), (7, 1), (6, 5), (9, 8), (7, 9), (4, 7),
        (1, 10), (2, 14),
    )),
    "circle": _east((
        (10, 0), (9.51, 3.09), (8.09, 5.88), (5.88, 8.09), (3.09, 9.51),
        (0, 10), (-3.09, 9.51), (-5.88, 8.09), (-8.09, 5.88), (-9.51, 3.09),
        (-10, 0), (-9.51, -3.09), (-8.09, -5.88), (-5.88, -8.09),
        (-3.09, -9.51), (0.0, -10.0), (3.09, -9.51), (5.88, -8.09),
        (8.09, -5.88), (9.51, -3.09),
    )),
    "square": _east(((10, -10), (10, 10), (-10, 10), (-10, -10))),
    "triangle": _east(((10, -5.77), (0, 11.55), (-10, -5.77))),
    "classic": _east(((0, 0), (-5, -9), (0, -7), (5, -9))),
}


def transform_polygon(poly, heading: float, stretch: tuple[float, float],
                      shear: float = 0.0, matrix=None) -> list[Point]:
    """چندضلعی کرسر را کش/برش/دوران می‌دهد — هنوز جابه‌جا نشده (مختصات نسبی).

    ساده‌سازی نسبت به فرمول داخلی turtle استاندارد: کش در راستای طول/عرض
    اعمال می‌شود، بعد برش به‌صورت sy += shear * sx، بعد دوران به‌اندازه‌ی
    heading. برای اکثر اسکریپت‌های آموزشی که shapesize/shearfactor را
    جداگانه صدا می‌زنند نتیجه‌ی یکسانی می‌دهد.

    اگر matrix داده شود (خروجی shapetransform)، به‌جای کش+برش مستقیم همان
    ماتریس ۲×۲ محلی اعمال می‌شود؛ heading همچنان روی نتیجه دوران می‌کند —
    یعنی لاک‌پشت با ماتریس دلخواه هم باز رو به جهت حرکتش می‌چرخد.
    """
    if matrix is not None:
        t11, t12, t21, t22 = matrix
        local = [(t11 * px + t12 * py, t21 * px + t22 * py) for px, py in poly]
    else:
        stretch_wid, stretch_len = stretch
        local = []
        for px, py in poly:
            sx = px * stretch_len   # در راستای جهت حرکت
            sy = py * stretch_wid + shear * (px * stretch_len)  # عمود + برش
            local.append((sx, sy))

    angle = math.radians(heading_to_arcade_angle(heading))
    cos_a, sin_a = math.cos(angle), math.sin(angle)
    return [(x * cos_a - y * sin_a, x * sin_a + y * cos_a) for x, y in local]


class Shape:
    """معادل turtle.Shape — نگهدارنده‌ی داده‌ی یک شکل کرسر."""

    _VALID_TYPES = ("polygon", "compound", "image")

    def __init__(self, type_, data=None):
        if type_ not in self._VALID_TYPES:
            raise ArcadeTurtleError(
                f"نوع Shape باید یکی از {self._VALID_TYPES} باشد، نه {type_!r}"
            )
        self.type = type_
        if type_ == "polygon":
            self.data = [tuple((float(x), float(y)) for x, y in data)] if data else []
        elif type_ == "compound":
            self.data = []
        else:  # image
            self.data = data  # مسیر فایل، به‌عنوان رشته

    def addcomponent(self, poly, fill, outline=None) -> None:
        if self.type != "compound":
            raise ArcadeTurtleError(
                "addcomponent() فقط روی Shape('compound') کار می‌کند."
            )
        if outline is None:
            outline = fill
        rgb_fill = resolve_color(fill)
        rgb_outline = resolve_color(outline)
        self.data.append(
            (tuple((float(x), float(y)) for x, y in poly), rgb_fill, rgb_outline)
        )


class ShapeRegistry:
    """رجیستری per-engine: شکل‌های آماده + هرچه کاربر با register_shape ثبت کند."""

    def __init__(self):
        self._shapes: dict[str, Shape] = {
            name: Shape("polygon", poly) for name, poly in BUILTIN_POLYGONS.items()
        }
        self._textures: dict[str, object] = {}

    def names(self) -> list[str]:
        return sorted(self._shapes)

    def get(self, name: str) -> Shape:
        if name not in self._shapes:
            available = ", ".join(self.names())
            raise ArcadeTurtleError(
                f"شکل '{name}' وجود ندارد. 🐢\nشکل‌های موجود: {available}"
            )
        return self._shapes[name]

    def get_texture(self, name: str):
        return self._textures.get(name)

    def bounding_radius(self, name: str, stretch: tuple[float, float]) -> float:
        """شعاع تقریبی کرسر — برای hit-test کلیک/کشیدن (Turtle.onclick/ondrag).

        ساده‌سازی: به‌جای برخورد دقیق نقطه-در-چندضلعی، یک دایره‌ی احاطه‌کننده
        استفاده می‌شود. برای اسکریپت‌های آموزشی که با کلیک روی لاک‌پشت تعامل
        می‌کنند (مثل Etch-A-Sketch) این دقت کافی است.
        """
        shape = self.get(name)
        scale = max(stretch)
        if shape.type == "image":
            texture = self._textures.get(name)
            if texture is None:
                return 10.0 * scale
            return math.hypot(texture.width, texture.height) / 2
        points = (shape.data[0] if shape.type == "polygon" else
                  [pt for poly, _, _ in shape.data for pt in poly])
        if not points:
            return 10.0 * scale
        return max(math.hypot(x, y) for x, y in points) * scale

    def register(self, name, shape=None) -> None:
        """معادل register_shape/addshape استاندارد:

        - register_shape("file.png")            → خودِ مسیر فایل، اسم شکل هم می‌شود
        - register_shape("name", "file.png")     → shape تصویری با اسم دلخواه
        - register_shape("name", [(x,y), ...])   → چندضلعی خام
        - register_shape("name", Shape(...))     → مستقیم (ساده یا compound)
        """
        if shape is None:
            if Path(name).suffix.lower() not in IMAGE_SUFFIXES:
                raise ArcadeTurtleError(
                    "register_shape با یک آرگومان فقط برای فایل تصویری (.gif یا .png) "
                    "است؛ برای چندضلعی هر دو آرگومان لازم است:\n"
                    "    register_shape(name, polygon)"
                )
            # نام ثبت‌شده دقیقاً همان رشته‌ی ورودی است (مثل stdlib) — نرمال‌سازی
            # مسیر (مثلاً / به \ در ویندوز) نباید اسم شکل را عوض کند
            self._register_image(name, name)
            return

        if isinstance(shape, str):
            self._register_image(name, shape)
            return

        if isinstance(shape, Shape):
            if shape.type == "image":
                self._register_image(name, shape.data)
            else:
                self._shapes[name] = shape
            return

        try:
            poly = tuple((float(x), float(y)) for x, y in shape)
        except (TypeError, ValueError):
            raise ArcadeTurtleError(
                f"شکل {shape!r} معتبر نیست؛ باید لیستی از (x, y) باشد، "
                "یا یک Shape، یا مسیر یک فایل تصویری."
            ) from None
        if len(poly) < 3:
            raise ArcadeTurtleError("چندضلعیِ شکل حداقل به ۳ نقطه نیاز دارد.")
        self._shapes[name] = Shape("polygon", poly)

    def _register_image(self, name: str, path: str) -> None:
        import arcade

        p = Path(path)
        if not p.exists():
            raise ArcadeTurtleError(
                f"فایل تصویر '{path}' پیدا نشد. مسیر را بررسی کن."
            )
        try:
            texture = arcade.load_texture(p)
        except Exception as e:
            raise ArcadeTurtleError(
                f"بارگذاری تصویر '{path}' شکست خورد: {e}"
            ) from None
        self._shapes[name] = Shape("image", str(p))
        self._textures[name] = texture
