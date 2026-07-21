"""Vec2D — برداری که position()/pos() برمی‌گرداند.

زیرکلاس tuple است تا هر کد قدیمی که `x, y = pos()` یا `pos() == (x, y)`
می‌نویسد بدون تغییر کار کند؛ علاوه بر آن جمع/تفریق/ضرب برداری و چرخش را
هم می‌دهد — همان چیزی که آموزش‌های فیزیک/بازی با آن `t.goto(t.pos() + Vec2D(0, 10))`
می‌نویسند.
"""

from __future__ import annotations

import math


class Vec2D(tuple):
    def __new__(cls, x, y):
        return tuple.__new__(cls, (x, y))

    def __add__(self, other):
        return Vec2D(self[0] + other[0], self[1] + other[1])

    def __sub__(self, other):
        return Vec2D(self[0] - other[0], self[1] - other[1])

    def __neg__(self):
        return Vec2D(-self[0], -self[1])

    def __mul__(self, other):
        """بردار×بردار = ضرب داخلی (عدد)؛ بردار×عدد = مقیاس‌شده (بردار)."""
        if isinstance(other, Vec2D):
            return self[0] * other[0] + self[1] * other[1]
        return Vec2D(self[0] * other, self[1] * other)

    def __rmul__(self, other):
        if isinstance(other, (int, float)):
            return Vec2D(self[0] * other, self[1] * other)
        return NotImplemented

    def __abs__(self):
        return math.hypot(*self)

    def rotate(self, angle):
        """چرخش پادساعتگرد به‌اندازه‌ی angle درجه (همان جهت left())."""
        perp = Vec2D(-self[1], self[0])
        rad = math.radians(angle)
        c, s = math.cos(rad), math.sin(rad)
        return Vec2D(self[0] * c + perp[0] * s, self[1] * c + perp[1] * s)

    def __repr__(self):
        return f"({self[0]:.2f},{self[1]:.2f})"
