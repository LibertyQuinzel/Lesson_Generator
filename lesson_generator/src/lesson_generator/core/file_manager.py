"""File and directory management for generated lessons."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional


@dataclass
class CreatePathsResult:
    root: Path
    modules: list[Path]


class FileStructureManager:
    """Creates directory structure and writes files for lessons."""

    def ensure_dir(self, path: Path) -> None:
        path.mkdir(parents=True, exist_ok=True)

    def create_lesson_dirs(self, base_dir: Path, topic_name: str, module_names: Iterable[str]) -> CreatePathsResult:
        root = base_dir / topic_name
        self.ensure_dir(root)
        modules: list[Path] = []
        for idx, mod in enumerate(module_names, start=1):
            mod_path = root / f"module_{idx}_{mod}"
            self.ensure_dir(mod_path)
            modules.append(mod_path)
        return CreatePathsResult(root=root, modules=modules)

    def write_text(self, path: Path, content: str) -> None:
        """Write text to file.

        Writes content exactly as provided without adding any artificial headers.
        """
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
