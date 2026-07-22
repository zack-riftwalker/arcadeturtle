"""تبدیل مختصات و زاویه بین دنیای Turtle و دنیای Arcade.

قرارداد Turtle: مبدأ وسط صفحه، y به بالا، زاویه صفر = شرق، درجه پادساعتگرد.
قرارداد Arcade: مبدأ گوشه پایین-چپ، y به بالا.

هیچ‌جای دیگر پروژه نباید width/2 یا height/2 اضافه کند — فقط اینجا.
"""

from __future__ import annotations

# مختصات جهانی دلخواه (setworldcoordinates): (llx, lly, urx, ury) یا None
# برای حالت پیش‌فرض. وقتی فعال است، این مستطیل به کل پنجره کشیده می‌شود —
# اگر نسبت x/y آن با نسبت پنجره یکی نباشد، زاویه‌ها کج‌نما می‌شوند؛ همان
# چیزی که خودِ turtle استاندارد هم صراحتاً هشدار می‌دهد.
World = tuple[float, float, float, float]


def to_arcade(tx: float, ty: float, width: int, height: int,
             world: World | None = None) -> tuple[float, float]:
    if world is None:
        return tx + width / 2, ty + height / 2
    llx, lly, urx, ury = world
    ax = (tx - llx) / (urx - llx) * width
    ay = (ty - lly) / (ury - lly) * height
    return ax, ay


def to_turtle(ax: float, ay: float, width: int, height: int,
             world: World | None = None) -> tuple[float, float]:
    if world is None:
        return ax - width / 2, ay - height / 2
    llx, lly, urx, ury = world
    tx = ax / width * (urx - llx) + llx
    ty = ay / height * (ury - lly) + lly
    return tx, ty


def heading_to_arcade_angle(heading: float) -> float:
    """زاویه turtle (پادساعتگرد از شرق) → زاویه دوران چندضلعی کرسر.

    چندضلعی‌های کرسر در _renderer «رو به شرق» تعریف شده‌اند و با ماتریس دوران
    استاندارد (پادساعتگرد) چرخانده می‌شوند؛ پس heading مستقیم قابل استفاده است.
    اگر روزی Sprite تصویری اضافه شد (Sprite.angle در Arcade 3 ساعتگرد است)،
    تبدیلش فقط همین‌جا اضافه می‌شود.
    """
    return heading
