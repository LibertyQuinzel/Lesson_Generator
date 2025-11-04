from __future__ import annotations

from pathlib import Path

from lesson_generator.core.template_engine import TemplateEngine


def test_render_readme_template(tmp_path: Path):
    # Arrange: create a tiny template in a temp dir
    templates_dir = tmp_path
    (templates_dir / "readme.md.j2").write_text("# {{ topic.title }}\n{{ topic.description }}\n", encoding="utf-8")

    engine = TemplateEngine(templates_dir)
    content = engine.render(
        "readme.md.j2",
        {"topic": {"title": "My Topic", "description": "Desc"}},
    )

    assert "# My Topic" in content
    assert "Desc" in content
