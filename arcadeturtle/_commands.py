"""فرمان‌های صف — واحدهای پخش انیمیشن در Engine.

هر فراخوانی API کاربر در حالت RECORDING یکی از این‌ها را به صف سراسری اضافه می‌کند.
ترتیب صف = ترتیب فراخوانی برنامه (یک صف واحد برای همه لاک‌پشت‌ها).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

Point = tuple[float, float]
Color = tuple[int, int, int]


@dataclass
class MoveCmd:
    """حرکت خطی (forward/backward/goto). انیمیشن با سرعت خطی."""
    turtle_id: int
    start: Point
    end: Point
    pen_down: bool
    color: Color
    size: int
    speed: int  # سرعت لاک‌پشت در لحظه ثبت فرمان


@dataclass
class RotateCmd:
    """چرخش (left/right/setheading). انیمیشن با سرعت زاویه‌ای."""
    turtle_id: int
    start_heading: float
    end_heading: float
    delta: float  # علامت‌دار: مثبت = پادساعتگرد؛ اندازه واقعی چرخش
    speed: int


@dataclass
class InstantCmd:
    """فرمان بدون انیمیشن (penup، رنگ، dot، write، ...).

    fn وقتی نوبتش در صف رسید اجرا می‌شود تا ترتیب دیداری حفظ شود.
    """
    turtle_id: int
    fn: Callable[[], None]
