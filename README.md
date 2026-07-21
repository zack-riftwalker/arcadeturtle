# ArcadeTurtle 🐢

کتابخانه‌ای آموزشی: همان دستورهای ماژول استاندارد `turtle` پایتون، اما با
موتور گرافیکی مدرن **[Arcade](https://api.arcade.academy/)** — حرکت نرم،
پنجره باکیفیت، و پشتیبانی کامل از متن فارسی در `write()`.

![نمونه خروجی ArcadeTurtle](docs/screenshot.png)

## نصب

```bash
python -m venv .venv
.venv\Scripts\activate        # ویندوز
pip install -e .
```

## شروع سریع

```python
import arcadeturtle as turtle

for _ in range(4):
    turtle.forward(100)
    turtle.left(90)

turtle.done()
```

همین! هر برنامه‌ای که با ماژول `turtle` استاندارد نوشته باشی، معمولاً فقط با
تغییر همین یک خط `import` روی ArcadeTurtle هم اجرا می‌شود.

## مثال‌ها

مثال‌ها در پوشه‌ی [`examples/`](examples/) از ساده به پیشرفته مرتب‌اند:

| فایل | چه چیزی یاد می‌دهد |
|---|---|
| [`00_healthcheck.py`](examples/00_healthcheck.py) | آیا Arcade و متن فارسی روی سیستم تو کار می‌کنند؟ |
| [`01_square.py`](examples/01_square.py) | اولین حرکت، چرخش و حلقه |
| [`02_star.py`](examples/02_star.py) | ستاره پنج‌پر، رنگ پس‌زمینه |
| [`03_polygon_function.py`](examples/03_polygon_function.py) | نوشتن تابع با پارامتر |
| [`04_color_spiral.py`](examples/04_color_spiral.py) | حلقه‌های تودرتو، `speed(0)` |
| [`05_filled_shapes.py`](examples/05_filled_shapes.py) | `begin_fill`/`end_fill`، `dot`، نوشتن فارسی |
| [`06_keyboard_drive.py`](examples/06_keyboard_drive.py) | کنترل با کیبورد (`onkeypress`) |
| [`07_click_paint.py`](examples/07_click_paint.py) | رویداد کلیک موس (`onscreenclick`) |
| [`08_snake_game.py`](examples/08_snake_game.py) | بازی کامل مار، چند لاک‌پشت، تابلوی امتیاز فارسی |
| [`golden_snake_original.py`](examples/golden_snake_original.py) | یک اسکریپت مار به سبک رایج اینترنتی — فقط با تغییر `import` اجرا می‌شود |

## جدول سازگاری با ماژول `turtle` استاندارد

### ✅ کامل پشتیبانی می‌شود

حرکت: `forward`/`fd`، `backward`/`bk`/`back`، `left`/`lt`، `right`/`rt`،
`goto`/`setpos`/`setposition`، `setx`، `sety`، `home`، `setheading`/`seth` •
قلم: `penup`/`pu`/`up`، `pendown`/`pd`/`down`، `isdown`، `pensize`/`width`،
`pencolor`، `speed` • ترسیم: `circle`، `dot`، `stamp`، `clearstamp`،
`clearstamps`، `begin_fill`، `end_fill`، `filling`، `fillcolor`، `color`،
`write` (با پشتیبانی فارسی خودکار) • ظاهر: `shape`، `shapesize`/`turtlesize`،
`hideturtle`/`ht`، `showturtle`/`st`، `isvisible` • کوئری: `position`/`pos`،
`xcor`، `ycor`، `heading`، `towards`، `distance` • رویداد: `listen`، `onkey`،
`onkeypress`، `onkeyrelease`، `onclick`/`onscreenclick`، `ontimer`، `tracer`،
`update` • صفحه: `bgcolor`، `title`، `clear`، `reset`، `done`/`mainloop` •
کلاس‌ها: `Turtle()` (چند نمونه مستقل)، `Screen()` (سینگلتون) با `setup`،
`window_width`/`window_height`، `exitonclick`، `bye`.

### 🟡 رفتار کمی متفاوت

- **`speed`**: عدد بین ۰ تا ۱۰ (یا نام‌های `fastest`/`fast`/`normal`/`slow`/
  `slowest`)؛ سرعت واقعی پیکسل بر ثانیه با turtle اصلی یکی نیست، ولی معنای
  نسبی (بزرگ‌تر = سریع‌تر، ۰ = آنی) همان است.
- **رنگ با اعداد اعشاری**: به‌جای فراخوانی `colormode(1.0)`، هر رنگی که سه عدد
  بین ۰ و ۱ باشد خودکار به‌عنوان اعشاری شناسایی می‌شود.
- **`shape`**: فقط شکل‌های آماده (`classic`, `arrow`, `turtle`, `circle`,
  `square`, `triangle`) — نه تصویر GIF مثل turtle اصلی.

### ❌ هنوز پشتیبانی نمی‌شود

`setworldcoordinates`، `register_shape`/`addshape` (شکل سفارشی)، `bgpic`،
`undo`/`setundobuffer`، `tiltangle`/`tilt`، `mode`، `colormode` به‌عنوان یک
حالت سراسری، `textinput`/`numinput`، `getscreen()` چندپنجره‌ای (فقط یک پنجره
در هر زمان). این‌ها همگی به‌صراحت خطای فارسی مهربان می‌دهند، نه رفتار خاموش
یا نادرست.

## پشت صحنه چطور کار می‌کند؟

سه تصمیم معماری کلیدی (شرح کامل در [ROADMAP.md](ROADMAP.md)):

1. **صف فرمان واحد**: هر فراخوانی دستور یک «فرمان» به یک صف FIFO مشترک
   اضافه می‌کند. وضعیت منطقی لاک‌پشت (برای `position()` و مانند آن) بلافاصله
   به‌روز می‌شود؛ پخش انیمیشنِ آن روی صفحه در فریم‌های بعدی انجام می‌شود.
2. **تبدیل مختصات متمرکز**: تنها در `_coords.py` — مبدأ Turtle وسط صفحه،
   مبدأ Arcade گوشه پایین-چپ.
3. **بافر خط پخته‌شده**: خط‌های تمام‌شده یک‌بار در `ShapeElementList` Arcade
   ساخته می‌شوند تا نقاشی‌های پیچیده (مثل مارپیچ) کند نشوند.

## اجرای تست‌ها

```bash
pip install -e ".[dev]"
pytest
```
