import pytest

from lesson_generator.core.generator import LessonGenerator


def test_is_valid_import_line_accepts_safe_imports():
    assert LessonGenerator._is_valid_import_line("import typing")
    assert LessonGenerator._is_valid_import_line("import typing as t")
    assert LessonGenerator._is_valid_import_line("from typing import Any, Iterable")


def test_is_valid_import_line_rejects_dangerous_or_invalid():
    assert not LessonGenerator._is_valid_import_line("import os")
    assert not LessonGenerator._is_valid_import_line("from subprocess import Popen")
    assert not LessonGenerator._is_valid_import_line("import requests")
    assert not LessonGenerator._is_valid_import_line("import math; print('x')")
    assert not LessonGenerator._is_valid_import_line("not an import")
