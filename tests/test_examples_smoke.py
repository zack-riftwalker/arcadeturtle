"""تست دود مثال‌ها: هر مثال باید پارس شود و فقط از API عمومی استفاده کند.

مثال‌ها را اجرا نمی‌کنیم (به پنجره نیاز دارند و mainloop بلاک می‌شود)، ولی
compile() خطای نحوی و import شکسته را زود می‌گیرد — مثال خراب بدترین چیزی
است که یک هنرجو می‌تواند ببیند.
"""

import ast
from pathlib import Path

import pytest

EXAMPLES = Path(__file__).resolve().parent.parent / "examples"
SCRIPTS = sorted(EXAMPLES.glob("*.py"))


def test_examples_directory_is_not_empty():
    assert SCRIPTS, f"هیچ مثالی در {EXAMPLES} پیدا نشد"


@pytest.mark.parametrize("path", SCRIPTS, ids=lambda p: p.name)
def test_example_compiles(path):
    source = path.read_text(encoding="utf-8")
    compile(source, str(path), "exec")


@pytest.mark.parametrize("path", SCRIPTS, ids=lambda p: p.name)
def test_example_only_imports_public_api(path):
    """هیچ مثالی نباید به ماژول‌های خصوصی (_engine, _renderer, ...) دست بزند."""
    tree = ast.parse(path.read_text(encoding="utf-8"), str(path))
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            assert "._" not in node.module and not node.module.startswith("_"), (
                f"{path.name} از ماژول خصوصی {node.module} استفاده می‌کند"
            )


def test_golden_snake_uses_only_stdlib_turtle_api():
    """ارزش آزمون طلایی به این است که «فقط import عوض شده» باشد.

    اگر کسی سهواً از یک API مخصوص ArcadeTurtle در آن استفاده کند، دیگر
    چیزی درباره سازگاری با turtle استاندارد ثابت نمی‌کند.
    """
    path = EXAMPLES / "golden_snake_original.py"
    tree = ast.parse(path.read_text(encoding="utf-8"), str(path))

    aliases = {
        n.asname or n.name
        for node in ast.walk(tree) if isinstance(node, ast.Import)
        for n in node.names
        if n.name == "arcadeturtle"
    }
    assert aliases == {"turtle"}, "باید دقیقاً به شکل «import arcadeturtle as turtle» باشد"

    used = {
        node.attr
        for node in ast.walk(tree)
        if isinstance(node, ast.Attribute)
        and isinstance(node.value, ast.Name)
        and node.value.id == "turtle"
    }
    # هرچه مستقیم روی ماژول turtle صدا زده می‌شود باید در stdlib هم وجود داشته باشد
    import turtle as std
    missing = {name for name in used if not hasattr(std, name)}
    assert not missing, f"این نام‌ها در turtle استاندارد وجود ندارند: {missing}"
