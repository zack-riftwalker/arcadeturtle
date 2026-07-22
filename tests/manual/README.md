# تست‌های دستی (نیازمند پنجره واقعی)

این اسکریپت‌ها بخشی از `pytest` نیستند، چون به یک پنجره‌ی واقعی Arcade و
OpenGL context نیاز دارند. آن‌ها را دستی اجرا کن — مخصوصاً بعد از تغییر در
`_engine.py`، `_renderer.py`، `_shapes.py` یا `_window.py` که تست‌های
headless نمی‌توانند کاملاً پوششان بدهند.

همه از ریشه‌ی مخزن اجرا می‌شوند:

```bash
# یک مثال را اجرا کن و وقتی نقاشی تمام شد عکس بگیر
.venv\Scripts\python.exe tests\manual\run_example_shot.py examples\01_square.py shot.png

# هر اسکریپتی را چند ثانیه اجرا کن و ببند (برای مثال‌هایی که حلقه‌شان تمام نمی‌شود)
.venv\Scripts\python.exe tests\manual\run_and_close.py examples\08_snake_game.py 2.5

# بازی مار را خودکار بازی کن: غذا بخور، به دیوار بزن، ریست را بررسی کن
.venv\Scripts\python.exe tests\manual\drive_snake.py

# آزمون طلایی: همان کار روی اسکریپت مارِ سبک اینترنتی
.venv\Scripts\python.exe tests\manual\drive_golden_snake.py

# فاز ۱۰.۸ — شش آزمون طلایی دیگر، هرکدام یک الگوی رایج اینترنتی را با
# تغییر فقط import اجرا و به‌صورت خودکار تعامل می‌کنند:
.venv\Scripts\python.exe tests\manual\drive_etch_a_sketch.py     # ondrag + کلیک راست
.venv\Scripts\python.exe tests\manual\drive_undo_drawing.py      # کیبورد + undo
.venv\Scripts\python.exe tests\manual\drive_pong.py              # بازی دونفره
.venv\Scripts\python.exe tests\manual\drive_space_invaders.py    # شکل تصویری + برخورد
.venv\Scripts\python.exe tests\manual\verify_shapes_visual.py    # چرخش شکل تصویری/ترکیبی/tilt
.venv\Scripts\python.exe tests\manual\verify_world_bgpic_visual.py  # bgpic + setworldcoordinates
.venv\Scripts\python.exe tests\manual\verify_drag_visual.py      # کشیدن روی پنجره‌ی واقعی
```

اسکریپت‌های `drive_*` و `verify_*` خودشان assert دارند و اگر رفتار درست
نباشد با خطا خارج می‌شوند؛ عکس خروجی را هم در همین پوشه با پیشوند `_out_`
ذخیره می‌کنند (این فایل‌ها در `.gitignore` هستند).

**قبل از هر انتشار، این موارد را دستی چک کن:**

1. `examples/08_snake_game.py` را واقعاً بازی کن — غذا، رشد، برخورد، امتیاز فارسی.
2. `examples/13_pong.py` و `examples/14_space_invaders.py` را بازی کن.
3. `examples/10_etch_a_sketch.py` را با موس بکش.
4. `examples/06_keyboard_drive.py` — روانی پاسخ کلیدها.
5. `examples/07_click_paint.py` — درستی مختصات کلیک موس.
6. `examples/05_filled_shapes.py` — خوانا بودن متن فارسی (حروف چسبیده، جهت درست).
