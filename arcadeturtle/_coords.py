"""تبدیل مختصات و زاویه بین دنیای Turtle و دنیای Arcade.

قرارداد Turtle: مبدأ وسط صفحه، y به بالا، زاویه صفر = شرق، درجه پادساعتگرد.
قرارداد Arcade: مبدأ گوشه پایین-چپ، y به بالا.

هیچ‌جای دیگر پروژه نباید width/2 یا height/2 اضافه کند — فقط اینجا.
"""

from __future__ import annotations


def to_arcade(tx: float, ty: float, width: int, height: int) -> tuple[float, float]:
    return tx + width / 2, ty + height / 2


def to_turtle(ax: float, ay: float, width: int, height: int) -> tuple[float, float]:
    return ax - width / 2, ay - height / 2


def heading_to_arcade_angle(heading: float) -> float:
    """زاویه turtle (پادساعتگرد از شرق) → زاویه دوران چندضلعی کرسر.

    چندضلعی‌های کرسر در _renderer «رو به شرق» تعریف شده‌اند و با ماتریس دوران
    استاندارد (پادساعتگرد) چرخانده می‌شوند؛ پس heading مستقیم قابل استفاده است.
    اگر روزی Sprite تصویری اضافه شد (Sprite.angle در Arcade 3 ساعتگرد است)،
    تبدیلش فقط همین‌جا اضافه می‌شود.
    """
    return heading
