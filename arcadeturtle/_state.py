"""TurtleState — وضعیت منطقی یک لاک‌پشت. ریاضی خالص، بدون هیچ وابستگی به Arcade."""

from __future__ import annotations

import math
from dataclasses import dataclass, field


@dataclass
class TurtleState:
    x: float = 0.0
    y: float = 0.0
    heading: float = 0.0  # درجه، پادساعتگرد، صفر = شرق
    pen_down: bool = True
    pen_color: tuple[int, int, int] = (0, 0, 0)
    pen_size: int = 1
    fill_color: tuple[int, int, int] = (0, 0, 0)
    speed: int = 3
    visible: bool = True
    shape: str = "classic"
    shape_size: tuple[float, float] = (1.0, 1.0)
    filling: bool = False
    fill_points: list[tuple[float, float]] = field(default_factory=list)

    def move_forward(self, dist: float) -> tuple[tuple[float, float], tuple[float, float]]:
        """حرکت به جلو در جهت heading. برمی‌گرداند (نقطه قبل، نقطه بعد)."""
        old = (self.x, self.y)
        rad = math.radians(self.heading)
        self.x += dist * math.cos(rad)
        self.y += dist * math.sin(rad)
        return old, (self.x, self.y)

    def rotate(self, delta_deg: float) -> None:
        """چرخش پادساعتگرد (delta منفی = ساعتگرد)، نرمال‌شده به [0, 360)."""
        self.heading = (self.heading + delta_deg) % 360.0

    def goto(self, x: float, y: float) -> tuple[tuple[float, float], tuple[float, float]]:
        old = (self.x, self.y)
        self.x, self.y = float(x), float(y)
        return old, (self.x, self.y)

    def set_heading(self, deg: float) -> None:
        self.heading = float(deg) % 360.0

    def towards(self, x: float, y: float) -> float:
        return math.degrees(math.atan2(y - self.y, x - self.x)) % 360.0

    def distance_to(self, x: float, y: float) -> float:
        return math.hypot(x - self.x, y - self.y)

    def copy_pose(self) -> "TurtleState":
        """کپی مستقل برای وضعیت بصری (visual state)."""
        c = TurtleState(**{k: getattr(self, k) for k in (
            "x", "y", "heading", "pen_down", "pen_color", "pen_size",
            "fill_color", "speed", "visible", "shape", "shape_size", "filling",
        )})
        c.fill_points = list(self.fill_points)
        return c
