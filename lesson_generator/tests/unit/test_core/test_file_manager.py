from __future__ import annotations

from lesson_generator.core.file_manager import FileStructureManager


def test_create_lesson_dirs(tmp_path):
    fm = FileStructureManager()
    res = fm.create_lesson_dirs(tmp_path, "async_programming", ["basics", "advanced"])
    assert res.root.exists()
    assert len(res.modules) == 2
    assert res.modules[0].name.startswith("module_1_basics")
