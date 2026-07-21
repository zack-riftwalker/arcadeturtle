"""رجیستری رویدادها — نسخه کامل در فاز ۵؛ فعلاً اسکلت بدون رفتار."""

from __future__ import annotations


class EventRegistry:
    def __init__(self, engine):
        self.engine = engine

    def handle_key_press(self, key) -> None:
        pass

    def handle_key_release(self, key) -> None:
        pass

    def handle_click(self, x, y, button) -> None:
        pass
