from pathlib import Path
from textwrap import dedent

from lesson_generator.core.template_engine import TemplateEngine


class BadStr:
    def __str__(self) -> str:  # type: ignore[override]
        raise RuntimeError("boom")


def test_docstring_filter_handles_str_exception(tmp_path: Path):
    # Create a tiny template that applies the docstring filter
    tpl_dir = tmp_path / "tpls"
    tpl_dir.mkdir()
    (tpl_dir / "t.j2").write_text("{{ val|docstring }}")

    engine = TemplateEngine(tpl_dir)
    # When __str__ raises, filter should fall back to empty string
    out = engine.render("t.j2", {"val": BadStr()})
    assert out == ""


def test_docstring_filter_escapes_triple_quotes_and_crlf(tmp_path: Path):
    tpl_dir = tmp_path / "tpls"
    tpl_dir.mkdir(exist_ok=True)
    (tpl_dir / "t.j2").write_text("{{ val|docstring }}")

    engine = TemplateEngine(tpl_dir)
    val = 'Line1\r\nLine2 with triple """ quotes'
    out = engine.render("t.j2", {"val": val})
    # Windows newlines normalized
    assert "\r\n" not in out and "Line1\nLine2" in out
    # Triple quotes escaped
    assert '\\"\"\"' in out
