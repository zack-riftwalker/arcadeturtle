"""رندر: بافر خط‌های پخته‌شده، پرکردن‌ها، مهرها، متن‌ها و کرسر لاک‌پشت‌ها.

همه مختصات ورودی این ماژول «مختصات Turtle» هستند؛ تبدیل به Arcade موقع رسم/بازسازی
انجام می‌شود تا تغییر اندازه پنجره (Screen.setup) بافر را خراب نکند.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import arcade
from arcade.shape_list import ShapeElementList, create_line, create_polygon

from ._coords import heading_to_arcade_angle, to_arcade

Point = tuple[float, float]
Color = tuple[int, int, int]

# چندضلعی‌های کرسر، برگرفته از _shapes ماژول turtle استاندارد CPython.
# آنجا «رو به شمال» تعریف شده‌اند؛ اینجا با تبدیل (x, y) -> (y, -x) رو به شرق
# ذخیره شده‌اند تا دوران پادساعتگرد با خودِ heading جهت درست را بدهد.
def _east(points: tuple[tuple[float, float], ...]) -> tuple[tuple[float, float], ...]:
    return tuple((y, -x) for x, y in points)


SHAPE_POLYGONS: dict[str, tuple[tuple[float, float], ...]] = {
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


@dataclass
class _Line:
    turtle_id: int
    start: Point
    end: Point
    color: Color
    width: float


@dataclass
class _Fill:
    turtle_id: int
    points: list[Point]
    color: Color


@dataclass
class _Stamp:
    stamp_id: int
    turtle_id: int
    shape: str
    x: float
    y: float
    heading: float
    stretch: tuple[float, float]
    fill: Color
    outline: Color


@dataclass
class _TextItem:
    turtle_id: int
    text: "arcade.Text"


def transform_shape(shape: str, heading: float,
                    stretch: tuple[float, float]) -> list[tuple[float, float]]:
    """چندضلعی کرسر را مقیاس و دوران می‌دهد (هنوز جابه‌جا نشده — مختصات نسبی)."""
    stretch_wid, stretch_len = stretch
    angle = math.radians(heading_to_arcade_angle(heading))
    cos_a, sin_a = math.cos(angle), math.sin(angle)
    out = []
    for px, py in SHAPE_POLYGONS[shape]:
        sx = px * stretch_len   # در راستای جهت حرکت
        sy = py * stretch_wid   # عمود بر جهت حرکت
        out.append((sx * cos_a - sy * sin_a, sx * sin_a + sy * cos_a))
    return out


class Renderer:
    def __init__(self, width: int = 800, height: int = 600):
        self.width = width
        self.height = height
        self.finished_lines: list[_Line] = []
        self.fills: list[_Fill] = []
        self.stamps: list[_Stamp] = []
        self.texts: list[_TextItem] = []
        self.live_line: _Line | None = None
        self._dirty = True
        self._shape_list: ShapeElementList | None = None
        self._next_stamp_id = 1

    # ---------- تغذیه بافر (مختصات Turtle) ----------

    def set_size(self, width: int, height: int) -> None:
        self.width, self.height = width, height
        self._dirty = True

    def add_line(self, turtle_id: int, start: Point, end: Point, color: Color,
                 width: float) -> None:
        self.finished_lines.append(_Line(turtle_id, start, end, color, width))
        self._dirty = True

    def add_fill(self, turtle_id: int, points: list[Point], color: Color) -> None:
        if len(points) >= 3:
            self.fills.append(_Fill(turtle_id, list(points), color))
            self._dirty = True

    def reserve_stamp_id(self) -> int:
        sid = self._next_stamp_id
        self._next_stamp_id += 1
        return sid

    def add_stamp(self, stamp_id: int, turtle_id: int, shape: str, x: float, y: float,
                  heading: float, stretch: tuple[float, float], fill: Color,
                  outline: Color) -> None:
        self.stamps.append(
            _Stamp(stamp_id, turtle_id, shape, x, y, heading, stretch, fill, outline)
        )

    def clear_stamp(self, stamp_id: int) -> None:
        self.stamps = [s for s in self.stamps if s.stamp_id != stamp_id]

    def clear_stamps_of(self, turtle_id: int, n: int | None = None) -> None:
        mine = [s for s in self.stamps if s.turtle_id == turtle_id]
        if n is None or n == 0:
            remove = set(id(s) for s in mine)
        elif n > 0:
            remove = set(id(s) for s in mine[:n])
        else:
            remove = set(id(s) for s in mine[n:])
        self.stamps = [s for s in self.stamps if id(s) not in remove]

    def add_text(self, turtle_id: int, text: "arcade.Text") -> None:
        self.texts.append(_TextItem(turtle_id, text))

    def set_live_line(self, start: Point, end: Point, color: Color, width: float) -> None:
        self.live_line = _Line(-1, start, end, color, width)

    def clear_live_line(self) -> None:
        self.live_line = None

    def clear_all(self) -> None:
        """معادل Screen.clear() — همه‌چیز از همه لاک‌پشت‌ها پاک می‌شود."""
        self.finished_lines.clear()
        self.fills.clear()
        self.stamps.clear()
        self.texts.clear()
        self.live_line = None
        self._dirty = True

    def clear_turtle(self, turtle_id: int) -> None:
        """معادل Turtle.clear() — فقط نقاشی‌های همین لاک‌پشت پاک می‌شود."""
        self.finished_lines = [ln for ln in self.finished_lines if ln.turtle_id != turtle_id]
        self.fills = [f for f in self.fills if f.turtle_id != turtle_id]
        self.stamps = [s for s in self.stamps if s.turtle_id != turtle_id]
        self.texts = [t for t in self.texts if t.turtle_id != turtle_id]
        self._dirty = True

    # ---------- رسم ----------

    def _to_a(self, p: Point) -> tuple[float, float]:
        return to_arcade(p[0], p[1], self.width, self.height)

    def _rebuild(self) -> None:
        sl = ShapeElementList()
        # اول پرکردن‌ها تا خط‌های مرزی رویشان دیده شوند (رفتار turtle)
        for f in self.fills:
            sl.append(create_polygon([self._to_a(p) for p in f.points], (*f.color, 255)))
        for ln in self.finished_lines:
            x1, y1 = self._to_a(ln.start)
            x2, y2 = self._to_a(ln.end)
            sl.append(create_line(x1, y1, x2, y2, (*ln.color, 255), ln.width))
        self._shape_list = sl
        self._dirty = False

    def _draw_cursor_polygon(self, shape: str, x: float, y: float, heading: float,
                             stretch: tuple[float, float], fill: Color,
                             outline: Color) -> None:
        ax, ay = self._to_a((x, y))
        pts = [(ax + dx, ay + dy) for dx, dy in transform_shape(shape, heading, stretch)]
        arcade.draw_polygon_filled(pts, fill)
        arcade.draw_polygon_outline(pts, outline, 1)

    def draw(self, turtle_states) -> None:
        """turtle_states: وضعیت‌های بصری قابل‌نمایش (iterable of TurtleState)."""
        if self._dirty or self._shape_list is None:
            self._rebuild()
        self._shape_list.draw()
        if self.live_line is not None:
            ln = self.live_line
            x1, y1 = self._to_a(ln.start)
            x2, y2 = self._to_a(ln.end)
            arcade.draw_line(x1, y1, x2, y2, ln.color, ln.width)
        for s in self.stamps:
            self._draw_cursor_polygon(s.shape, s.x, s.y, s.heading, s.stretch,
                                      s.fill, s.outline)
        for t in self.texts:
            t.text.draw()
        for st in turtle_states:
            if st.visible:
                self._draw_cursor_polygon(st.shape, st.x, st.y, st.heading,
                                          st.shape_size, st.fill_color, st.pen_color)
