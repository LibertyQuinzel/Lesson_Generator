"""Template engine for rendering lesson files."""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from jinja2 import Environment, FileSystemLoader, select_autoescape


class TemplateEngine:
    """Wrapper around Jinja2 environment for rendering templates."""

    def __init__(self, templates_dir: Path) -> None:
        self.templates_dir = templates_dir
        # Disable autoescaping globally since we render Python code templates; markdown doesn't need HTML escaping either.
        self.env = Environment(
            loader=FileSystemLoader(str(templates_dir)),
            autoescape=False,
            trim_blocks=True,
            lstrip_blocks=True,
        )
        # Register small safety filters for embedding AI text inside Python triple-quoted docstrings
        def _docstring_filter(value: Any) -> str:
            try:
                s = str(value if value is not None else "")
            except Exception:
                s = ""
            # Replace triple double-quotes which would terminate a Python docstring
            s = s.replace('"""', '\\"\"\"')
            # Also normalize Windows newlines
            s = s.replace('\r\n', '\n')
            return s

        self.env.filters["docstring"] = _docstring_filter

    def render(self, template_name: str, context: Dict[str, Any]) -> str:
        template = self.env.get_template(template_name)
        return template.render(**context)
