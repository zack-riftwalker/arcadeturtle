"""پشتیبانی متن فارسی: اتصال حروف (reshaping) و راست‌به‌چپ (bidi)."""

from __future__ import annotations

import re

import arabic_reshaper
from bidi.algorithm import get_display

# محدوده‌های یونیکد عربی/فارسی
_ARABIC = re.compile(r"[؀-ۿݐ-ݿﭐ-﷿ﹰ-﻿]")

PERSIAN_FONT = "Vazirmatn"


def has_persian(text: str) -> bool:
    return bool(_ARABIC.search(text))


def shape_text(text: str) -> str:
    """متن فارسی را برای رندر آماده می‌کند؛ متن لاتین دست‌نخورده می‌ماند."""
    if has_persian(text):
        return get_display(arabic_reshaper.reshape(text))
    return text
