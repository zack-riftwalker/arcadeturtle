"""Engine — قلب کتابخانه: صف فرمان، پخش انیمیشن، مدیریت پنجره و لاک‌پشت‌ها.

مدل اجرا (تصمیم ۱ پلن، ساده‌شده):
- state «منطقی» هر لاک‌پشت همان لحظه‌ی فراخوانی API آپدیت می‌شود تا
  کوئری‌هایی مثل position()/heading() همیشه جواب درست بدهند.
- هر فرمان دیداری وارد یک صف واحد FIFO می‌شود (چه در اسکریپت، چه در callback).
- tick() هر فریم صف را خالی می‌کند: با انیمیشن روی state «بصری»، یا آنی
  (speed == 0 یا tracer(0)). چون callback ها هم به همین صف می‌ریزند، به حالت
  LIVE جداگانه نیازی نیست — ترتیب همیشه حفظ است.
"""

from __future__ import annotations

import atexit
import math
from collections import deque
from dataclasses import dataclass
from enum import Enum

from ._commands import InstantCmd, MoveCmd, RotateCmd
from ._events import EventRegistry
from ._renderer import Renderer
from ._state import TurtleState

# سرعت‌های پخش (جدول قطعی پلن)
MOVE_PX_PER_SEC = 250
ROTATE_DEG_PER_SEC = 400


class Mode(Enum):
    RECORDING = "recording"  # قبل از done()
    PLAYING = "playing"      # داخل حلقه arcade


@dataclass
class TurtleRuntime:
    logical: TurtleState
    visual: TurtleState


class Engine:
    def __init__(self):
        self.mode = Mode.RECORDING
        self.queue: deque = deque()
        self.turtles: dict[int, TurtleRuntime] = {}
        self.active_cmd = None
        self._progress = 0.0
        self.tracer_n = 1
        self.renderer = Renderer()
        self.events = EventRegistry(self)
        self.window = None
        # تنظیمات پنجره قبل از ساخته‌شدنش
        self.pending_width = 800
        self.pending_height = 600
        self.pending_title = "ArcadeTurtle"
        self.pending_bg = (255, 255, 255)
        self._next_turtle_id = 0
        self._ran = False

    # ---------- لاک‌پشت‌ها ----------

    def new_turtle(self) -> int:
        tid = self._next_turtle_id
        self._next_turtle_id += 1
        st = TurtleState()
        self.turtles[tid] = TurtleRuntime(logical=st, visual=st.copy_pose())
        return tid

    def visible_states(self):
        return [rt.visual for rt in self.turtles.values()]

    # ---------- پنجره ----------

    def ensure_window(self):
        if self.window is None:
            from ._window import ArcadeTurtleWindow
            self.window = ArcadeTurtleWindow(
                self, self.pending_width, self.pending_height, self.pending_title
            )
            self.window.background_color = self.pending_bg
            self.renderer.set_size(self.pending_width, self.pending_height)
        return self.window

    def set_bgcolor(self, color) -> None:
        self.pending_bg = color
        if self.window is not None:
            self.window.background_color = color

    def set_title(self, text: str) -> None:
        self.pending_title = text
        if self.window is not None:
            self.window.set_caption(text)

    def run(self) -> None:
        """done()/mainloop() — پنجره را می‌سازد و حلقه arcade را شروع می‌کند."""
        if self._ran:
            return
        self._ran = True
        import arcade
        self.ensure_window()
        self.mode = Mode.PLAYING
        arcade.run()

    # ---------- صف و پخش ----------

    def submit(self, cmd) -> None:
        self.queue.append(cmd)

    def set_tracer(self, n: int) -> None:
        self.tracer_n = n
        if n == 0 and self.active_cmd is not None:
            # فرمان نیمه‌کاره فوراً تمام شود
            self.renderer.clear_live_line()
            self._apply_instant(self.active_cmd)
            self.active_cmd = None

    def tick(self, dt: float) -> None:
        remaining = dt
        while True:
            if self.active_cmd is None:
                if not self.queue:
                    return
                cmd = self.queue.popleft()
                if isinstance(cmd, InstantCmd):
                    cmd.fn()
                    continue
                if self.tracer_n == 0 or cmd.speed == 0:
                    self._apply_instant(cmd)
                    continue
                self.active_cmd = cmd
                self._progress = 0.0
            if remaining <= 0:
                return
            remaining = self._advance(remaining)
            if self.active_cmd is not None:
                return  # فرمان فعال هنوز تمام نشده؛ فریم بعد ادامه می‌یابد

    def _visual(self, turtle_id: int) -> TurtleState:
        return self.turtles[turtle_id].visual

    def _apply_instant(self, cmd) -> None:
        v = self._visual(cmd.turtle_id)
        if isinstance(cmd, MoveCmd):
            if cmd.pen_down:
                self.renderer.add_line(cmd.turtle_id, cmd.start, cmd.end, cmd.color, cmd.size)
            v.x, v.y = cmd.end
        elif isinstance(cmd, RotateCmd):
            v.heading = cmd.end_heading % 360.0

    def _advance(self, dt: float) -> float:
        """فرمان فعال را به‌اندازه dt جلو می‌برد؛ زمانِ مصرف‌نشده را برمی‌گرداند."""
        cmd = self.active_cmd
        v = self._visual(cmd.turtle_id)
        if isinstance(cmd, MoveCmd):
            length = math.dist(cmd.start, cmd.end)
            pps = cmd.speed * MOVE_PX_PER_SEC
            needed = (length - self._progress) / pps if pps > 0 else 0.0
            if dt >= needed or length == 0:
                self.renderer.clear_live_line()
                self._apply_instant(cmd)
                self.active_cmd = None
                return dt - needed
            self._progress += dt * pps
            t = self._progress / length
            cur = (
                cmd.start[0] + (cmd.end[0] - cmd.start[0]) * t,
                cmd.start[1] + (cmd.end[1] - cmd.start[1]) * t,
            )
            v.x, v.y = cur
            if cmd.pen_down:
                self.renderer.set_live_line(cmd.start, cur, cmd.color, cmd.size)
            return 0.0
        if isinstance(cmd, RotateCmd):
            total = abs(cmd.delta)
            dps = cmd.speed * ROTATE_DEG_PER_SEC
            needed = (total - self._progress) / dps if dps > 0 else 0.0
            if dt >= needed or total == 0:
                self._apply_instant(cmd)
                self.active_cmd = None
                return dt - needed
            self._progress += dt * dps
            sign = 1.0 if cmd.delta >= 0 else -1.0
            v.heading = (cmd.start_heading + sign * self._progress) % 360.0
            return 0.0
        # نوع ناشناخته — نباید رخ دهد
        self.active_cmd = None
        return dt


_engine: Engine | None = None
_atexit_registered = False


def _warn_if_done_forgotten() -> None:
    eng = _engine
    if eng is not None and not eng._ran and eng.turtles:
        import sys
        print(
            "\n⚠️  به نظر می‌رسد done() را فراموش کرده‌ای؛ "
            "بدون آن پنجره هرگز باز نمی‌شود.\n"
            "    آخرین خط برنامه‌ات را با turtle.done() تمام کن.\n",
            file=sys.stderr,
        )


def get_engine() -> Engine:
    global _engine, _atexit_registered
    if _engine is None:
        _engine = Engine()
        if not _atexit_registered:
            atexit.register(_warn_if_done_forgotten)
            _atexit_registered = True
    return _engine


def reset_engine() -> None:
    """فقط برای تست‌ها — موتور فعلی را «مصرف‌شده» علامت می‌زند تا هشدار
    فراموشیِ done() برای اسکریپت‌های آزمایشی که عمداً done() صدا نمی‌زنند
    نمایش داده نشود."""
    global _engine
    if _engine is not None:
        _engine._ran = True
    _engine = None
