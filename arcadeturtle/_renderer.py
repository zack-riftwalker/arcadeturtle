"""رندر: بافر خط‌های پخته‌شده، پرکردن‌ها، مهرها، متن‌ها و کرسر لاک‌پشت‌ها.

همه مختصات ورودی این ماژول «مختصات Turtle» هستند؛ تبدیل به Arcade موقع رسم/بازسازی
انجام می‌شود تا تغییر اندازه پنجره (Screen.setup) بافر را خراب نکند.
"""

from __future__ import annotations

from dataclasses import dataclass

import arcade
from arcade.shape_list import ShapeElementList, create_line, create_polygon
from arcade.types.rect import XYWH

from ._coords import heading_to_arcade_angle, to_arcade
from ._shapes import BUILTIN_POLYGONS, ShapeRegistry, transform_polygon

Point = tuple[float, float]
Color = tuple[int, int, int]

# متن‌ها تا وقتی صاحبشان clear() نزند باقی می‌مانند. الگوی «write داخل حلقه
# بدون clear» اشتباه رایج مبتدی است و نتیجه‌اش کندی تدریجی بدون هیچ پیامی؛
# پس یک‌بار هشدار می‌دهیم. هیچ متنی حذف نمی‌شود — فقط تشخیص.
TEXT_WARN_THRESHOLD = 1000

# سازگاری با کدهای قدیمی‌تر که مستقیم SHAPE_POLYGONS را ایمپورت می‌کردند —
# منبع اصلی حالا arcadeturtle._shapes.BUILTIN_POLYGONS است.
SHAPE_POLYGONS = BUILTIN_POLYGONS


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
    heading: float  # توجه: از قبل شامل tilt_angle است (heading نمایشی لحظه‌ی مهر)
    stretch: tuple[float, float]
    fill: Color
    outline: Color
    shear: float = 0.0
    outline_width: float = 1.0
    matrix: tuple[float, float, float, float] | None = None


@dataclass
class _TextItem:
    turtle_id: int
    text: "arcade.Text"


class Renderer:
    def __init__(self, width: int = 800, height: int = 600,
                 shapes: ShapeRegistry | None = None):
        self.width = width
        self.height = height
        self.shapes = shapes if shapes is not None else ShapeRegistry()
        self.finished_lines: list[_Line] = []
        self.fills: list[_Fill] = []
        self.stamps: list[_Stamp] = []
        self.texts: list[_TextItem] = []
        self.live_line: _Line | None = None
        self._dirty = True
        self._shape_list: ShapeElementList | None = None
        self._next_stamp_id = 1
        self._text_warned = False

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
                  outline: Color, shear: float = 0.0, outline_width: float = 1.0,
                  matrix=None) -> None:
        self.stamps.append(
            _Stamp(stamp_id, turtle_id, shape, x, y, heading, stretch, fill, outline,
                   shear, outline_width, matrix)
        )

    def clear_stamp(self, stamp_id: int) -> None:
        self.stamps = [s for s in self.stamps if s.stamp_id != stamp_id]

    def clear_stamps_of(self, turtle_id: int, n: int | None = None) -> None:
        """همان معناشناسی RawTurtle.clearstamps: None = همه، n >= 0 = n تای اول،
        n < 0 = n تای آخر. توجه: n == 0 برش خالی است و هیچ مهری پاک نمی‌شود."""
        mine = [s for s in self.stamps if s.turtle_id == turtle_id]
        if n is None:
            doomed = mine
        elif n >= 0:
            doomed = mine[:n]
        else:
            doomed = mine[n:]
        remove = {id(s) for s in doomed}
        self.stamps = [s for s in self.stamps if id(s) not in remove]

    def add_text(self, turtle_id: int, text: "arcade.Text") -> None:
        self.texts.append(_TextItem(turtle_id, text))
        if len(self.texts) > TEXT_WARN_THRESHOLD and not self._text_warned:
            self._text_warned = True
            import sys
            print(
                f"\n⚠️  بیش از {TEXT_WARN_THRESHOLD} متن روی صفحه جمع شده و "
                "برنامه کم‌کم کند می‌شود. 📝\n"
                "    اگر داخل حلقه write() می‌زنی، قبلش clear() را صدا بزن:\n"
                "        نویسنده.clear()\n"
                "        نویسنده.write(f\"امتیاز: {score}\")\n",
                file=sys.stderr,
            )

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

    # ---------- undo: حذف آخرین آیتمِ یک لاک‌پشتِ خاص ----------

    def _remove_last(self, items: list, turtle_id: int):
        for i in range(len(items) - 1, -1, -1):
            if items[i].turtle_id == turtle_id:
                item = items.pop(i)
                self._dirty = True
                return item
        return None

    def remove_last_line_of(self, turtle_id: int):
        return self._remove_last(self.finished_lines, turtle_id)

    def remove_last_fill_of(self, turtle_id: int):
        return self._remove_last(self.fills, turtle_id)

    def remove_last_text_of(self, turtle_id: int):
        return self._remove_last(self.texts, turtle_id)

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

    def _draw_shape(self, shape_name: str, x: float, y: float, heading: float,
                    stretch: tuple[float, float], fill: Color, outline: Color,
                    shear: float = 0.0, outline_width: float = 1.0,
                    matrix=None) -> None:
        """رسم کرسر/مهر بر اساس نوع شکل ثبت‌شده (polygon / compound / image)."""
        shape = self.shapes.get(shape_name)
        ax, ay = self._to_a((x, y))

        if shape.type == "image":
            self._draw_image_shape(shape_name, ax, ay, heading, stretch)
            return

        if shape.type == "compound":
            for poly, comp_fill, comp_outline in shape.data:
                pts = [(ax + dx, ay + dy) for dx, dy in
                       transform_polygon(poly, heading, stretch, shear, matrix)]
                arcade.draw_polygon_filled(pts, comp_fill)
                arcade.draw_polygon_outline(pts, comp_outline, outline_width)
            return

        # polygon ساده
        poly = shape.data[0] if shape.data else ()
        pts = [(ax + dx, ay + dy) for dx, dy in
               transform_polygon(poly, heading, stretch, shear, matrix)]
        arcade.draw_polygon_filled(pts, fill)
        arcade.draw_polygon_outline(pts, outline, outline_width)

    def _draw_image_shape(self, shape_name: str, ax: float, ay: float,
                          heading: float, stretch: tuple[float, float]) -> None:
        texture = self.shapes.get_texture(shape_name)
        if texture is None:
            return
        stretch_wid, stretch_len = stretch
        w = texture.width * stretch_len
        h = texture.height * stretch_wid
        rect = XYWH(ax, ay, w, h)
        angle = -heading_to_arcade_angle(heading)  # جهت چرخش تصویر در Arcade
        arcade.draw_texture_rect(texture, rect, angle=angle)

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
            self._draw_shape(s.shape, s.x, s.y, s.heading, s.stretch,
                             s.fill, s.outline, s.shear, s.outline_width, s.matrix)
        for t in self.texts:
            t.text.draw()
        for st in turtle_states:
            if st.visible:
                self._draw_shape(st.shape, st.x, st.y, st.heading + st.tilt_angle,
                                 st.shape_size, st.fill_color, st.pen_color,
                                 st.shear_factor, st.outline_width, st.shape_transform)
